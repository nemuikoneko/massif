from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    print('query is', query)

    results = {}

    main_resp = requests.get(f'http://localhost:9200/ja_sent_main/_search', json={
        'query': {
            'match_phrase': {
                'text': query,
            },
        },
        'highlight': {
            'fields': {
                'text': {},
            },
        },
    })
    main_resp.raise_for_status()

    main_resp_body = main_resp.json()

    hitcount_value =  main_resp_body['hits']['total']['value']
    if main_resp_body['hits']['total']['relation'] == 'eq':
        results['count_str'] = f'{hitcount_value}'
    elif main_resp_body['hits']['total']['relation'] == 'gte':
        results['count_str'] = f'>{hitcount_value}'
    else:
        assert False

    meta_ids = [hit['_source']['mid'] for hit in main_resp_body['hits']['hits']]

    if meta_ids:
        meta_resp = requests.get(f'http://localhost:9200/ja_sent_meta/_mget', json={'ids': meta_ids})
        meta_resp.raise_for_status()
        meta_resp_body = meta_resp.json()
        meta_map = {doc['_id']: doc['_source'] for doc in meta_resp_body['docs']}
    else:
        meta_map = {}

    results_list = []
    for hit in main_resp_body['hits']['hits']:
        xhit = {
            'markup': hit['highlight']['text'][0].replace('\n', '<br>')
        }
        mdata = meta_map.get(hit['_source']['mid'])
        if mdata:
            xhit['title'] = mdata['title']
        results_list.append(xhit)
    results['list'] = results_list

    return render_template('index.html', query=query, results=results)

application = app # for EB

if __name__ == "__main__":
    app.debug = True
    app.run()
