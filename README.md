# Massif - Curated, indexed content for foreign language learners

Massif is an umbrella project that contains a few different threads of work related to helping people learn foreign languages by **curating and indexing authentic foreign language content**.

https://massif.la/ja is the first available tool: a search engine for Japanese example sentences drawn from novels and dramas.

This repo contains a mix of a) reasonably coherent code to power the above site, and b) random scraps of research code, esp. around sentence scoring. It's probably not of much use to other people at this point, but I've made it public in the spirit of "working with the garage door up".

## Background

I generally subscribe to the [input hypothesis](https://en.wikipedia.org/wiki/Input_hypothesis) and have personally had success learning Japanese with a study method based on media immersion and sentence mining into [Anki](https://apps.ankiweb.net/) (similar to the [Refold](https://refold.la/) approach). But despite the abundance of tools available, the study process still has some conspicuous pain points, including:

* **Clunky sentence mining and card creation**: Even with the latest tools (which usually involve a lot of setup), mining sentences into Anki is clunky.
* **Mined sentences are of mixed quality**: Most sentences you encounter in immersion don't make for great sentence cards, for a variety of reasons. High quality sentences are worth their weight in gold.
* **Sentence cards don't age well**: Sentence cards tend to become less effective as their intervals grow larger, because you end up memorizing the context too much. In theory, once a have a word seeded in memory, it should mostly get reinforced by immersion (not just SRS), but this is still somewhat of an issue.
* **Difficulty finding incremental content**: For beginner/intermediate learners, it can be hard to find content that is at the right level of diffculty. One needs to learn to power through this to some extent, but it still could be improved.
* **Toolchain complexity**: Existing "all in one" products fail to encompass the whole process, so learners following this approach end up having to piece together a complicated chain of tools to get the job done. This allows for a lot of flexibility and customization, but excludes less tech-savvy learners and people who are curious to try the methods with less commitment.

It occurred to me that many (if not all) of the above issues could be addressed with a cluster of related tools and resources that revolve around the theme of **collecting, analyzing, scoring, and indexing** a large amount of language content. The content could be publicly accessible (e.g. news articles, YouTube, Netflix) or not (personal media collections). **Importantly**, we could **legally** collect and process all sorts of content as long as long as we only redistribute small excerpts to users, as it would squarely fall under **fair use** provisions (just as it is legal for Google to index the web, and [legal](https://en.wikipedia.org/wiki/Authors_Guild,_Inc._v._Google,_Inc.) for Google Books to scan and index books).

With a large amount of analyzed, index content, we can do things like:
* **Build a search engine for sentences**, for general reference, that (when possible) links back to the source content. There are already some other collections of "example sentences" ([Tatoeba](https://tatoeba.org/), [用例.jp](http://yourei.jp/)), but they all suffer from one issue or another (questionable quality/authenticity, antiquated sources, etc.).
* **Identify "high quality" sentences that are more likely to make for good flash cards.** *In my personal studies, when I encounter a new word in immersion, I've found myself increasingly often making a card from a dictionary example sentence for that word, rather than the sentence in which I encountered the word.* If you make a card with the sentence from your immersion, there is the benefit that you have a personal connection to it, but the downside that the sentence often doesn't stand well outside of the original context. Furthermore, having a database of high-quality sentences available for words would allow for study methods that don't require mining. Pre-made Anki decks are quite popular at the beginner/intermediate level (e.g. the famous "Core" Japanese decks), and are closely related to this. Having a high quality sentence database would allow for the automatic generation of such decks under customized parameters, e.g. for a certain target set of words, or only using sentences drawn from certain genres.
* **Recommend immersion content** suitable for a learner. With a large index of publicly available content and a list of words known by a user, we can find pieces of content that only use words they know, or are incremental to a specific degree. Per the previous point, learners could also pick a piece of content and "chart a course" for it, pre-learning the necessary words before ever seeing it.
* **Tie it all together.** It seems like this could all be tied together into a powerful learning tool that would also be simple to use. The tool would maintain a model of the learner's knowledge (as does Anki). It would present incremental flash cards derived from the sentence database (no mining required) that progress towards customizable goals, and link users out to publicly available immersion content that matches their specific knowledge.

*(to be continued)*