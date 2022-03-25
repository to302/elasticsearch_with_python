# Built-in analyzer reference
## [Standard Analyzer][9]
The standard analyzer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm. It removes most punctuation, lowercases terms, and supports removing stop words.

## [Simple Analyzer][10]
The simple analyzer divides text into terms whenever it encounters a character which is not a letter. It lowercases all terms.

## [Whitespace Analyzer][11]
The whitespace analyzer divides text into terms whenever it encounters any whitespace character. It does not lowercase terms.

## [Stop Analyzer][12]
The stop analyzer is like the simple analyzer, but also supports removal of stop words.

## [Keyword Analyzer][13]
The keyword analyzer is a “noop” analyzer that accepts whatever text it is given and outputs the exact same text as a single term.

## [Pattern Analyzer][14]
The pattern analyzer uses a regular expression to split the text into terms. It supports lower-casing and stop words.

## [Language Analyzers][15]
Elasticsearch provides many language-specific analyzers like `english` or `french`.

## [Fingerprint Analyzer][16]
The fingerprint analyzer is a specialist analyzer which creates a fingerprint which can be used for duplicate detection.



[9]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html "Standard Analyzer"
[10]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-simple-analyzer.html "Simple Analyzer"
[11]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-whitespace-analyzer.html "Whitespace Analyzer"
[12]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-analyzer.html "Stop Analyzer"
[13]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-keyword-analyzer.html "Keyword Analyzer"
[14]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pattern-analyzer.html "Pattern Analyzer"
[15]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html "Language Analyzers"
[16]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-fingerprint-analyzer.html "Fingerprint Analyzer"