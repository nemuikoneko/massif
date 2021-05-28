import json
import os
import sys
import tensorflow as tf
import argparse
from tensorflow.contrib.training import HParams

import model
from encode_bpe import BPEEncoder_ja

def score_tokens(*, hparams, tokens):
    # tokens is 1d, but model expects a batch of token-lists, so make a batch of 1
    x = tf.stack([tokens])

    lm_output = model.model(hparams=hparams, X=x, past=None, reuse=tf.AUTO_REUSE)

    # lm_output['logits'] should have shape [batch_size, tokens_length, vocab_size],
    # but from the slice in sample.py, it seemed like this might not always be the case?
    assert lm_output['logits'].shape[2] == hparams.n_vocab

    # take the first tensor, since batch size is fixed at 1
    logits = lm_output['logits'][0]
    # logits has shape [tokens_length, vocab_size]

    # get actual probabilities, in same shape as logits
    probs = model.softmax(logits)

    # The probabilities are for its guesses about the next token after each position.
    # We want to look up the probability that it gave for what actually turned out to be the "true"
    # next token.
    next_tokens = tokens[1:]
    tokens_range = tf.range(tf.shape(next_tokens)[0])
    indices = tf.stack([tokens_range, next_tokens], axis=-1)
    # indices has shape [next_tokens_length, 2]. it is a list of [pos, token] that we want to lookup in probs
    probs_next = tf.gather_nd(probs, indices)
    # probs_next has shape [tokens_length-1], and has the predicted probability of each input token (after the first one)

    # Get log probabilities
    ln_probs_next = tf.log(probs_next)

    return ln_probs_next

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('--model', default='gpt2ja-medium')
parser.add_argument('--gpu', type=str, default='0')
args = parser.parse_args()

with open('ja-bpe.txt') as f:
    bpe = f.read().split('\n')

with open('emoji.json') as f:
    emoji = json.loads(f.read())

enc = BPEEncoder_ja(bpe, emoji)
n_vocab = len(enc)

if 'small' in args.model:
    hparams = HParams(**{
      "n_vocab": n_vocab,
      "n_ctx": 1024,
      "n_embd": 768,
      "n_head": 12,
      "n_layer": 12
    })
elif 'medium' in args.model:
    hparams = HParams(**{
      "n_vocab": n_vocab,
      "n_ctx": 1024,
      "n_embd": 1024,
      "n_head": 16,
      "n_layer": 24
    })
elif 'large' in args.model:
    hparams = HParams(**{
      "n_vocab": n_vocab,
      "n_ctx": 1024,
      "n_embd": 1280,
      "n_head": 20,
      "n_layer": 36
    })
else:
    raise ValueError('invalid model name.')

# read input texts
if args.input_file == '-':
    input_f = sys.stdin
else:
    input_f = open(args.input_file, 'r')

texts = []
for line in input_f:
    sline = line.strip()
    if not sline:
        continue
    texts.append(sline)


config = tf.ConfigProto()

if int(args.gpu) >= 0:
    config.gpu_options.allow_growth = True
    config.gpu_options.visible_device_list = args.gpu

ADD_END_TOKEN = True

with tf.Session(config=config, graph=tf.Graph()) as sess:
    tokens_tensor = tf.placeholder(tf.int32, [None])

    output = score_tokens(hparams=hparams, tokens=tokens_tensor)

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(args.model)
    saver.restore(sess, ckpt)

    end_token = enc.encode('<|endoftext|>')[0]
    start_token = end_token # it does double duty

    for text in texts:
        # prepend the start token so that we get a probability for the first "real" token
        tokens = enc.encode(text)
        expanded_tokens = [start_token] + tokens
        if ADD_END_TOKEN:
            expanded_tokens += [end_token]

        logprobs = sess.run(output, feed_dict={
            tokens_tensor: expanded_tokens,
        })

        logprobs_list = logprobs.tolist()
        assert len(logprobs_list) == len(expanded_tokens) - 1 # sanity check

        sumlogprob = sum(logprobs_list)

        print('%s\t%.5g' % (text, sumlogprob), flush=True)
