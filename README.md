# Quantum Monitor Regulatory Comments Fetcher

## Getting Started

**[regulations.gov](regulations.gov) API Key**
https://open.gsa.gov/api/regulationsgov/

To begin using this API, you will need to register for an API Key below.

If you want to use commenting API, you *MUST* use the form below to register for an API key.

After registration, you will need to provide this API key in the X-Api-Key HTTP header with *every* API request.

## API Description

Regulations.gov offers a GET API for documents, comments, and dockets and a POST API for comments. These endpoints can be used for searching document, comments and dockets, and posting a comment. **Note:** We will only use the POST API since we're just pulling comments.

The quantum monitor searches for `comments` on the  quantum computing regulations `dockets`. 

### Searching for comments

You can search for a list of comments based on the criteria passed by using the endpoint `/v4/comments`. The search operation supports full text keyword searches and filtering based on a number of available parameters.

#### Detailed information for a single comment

In order to obtain more details about a single comment, you can use the endpoint `/v4/comments/{commentId}`. Each comment has its own set of attributes, which vary based on the Agency posting the comment. Another defining characteristic is if the comment is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

### Searching for dockets

A docket is an organizational folder containing multiple documents. Dockets can be searched using the endpoint: `/v4/dockets`.

#### Detailed information for a single docket

In order to obtain more details about a single docket, you can use the endpoint `/v4/dockets/{docketId}`. Each docket has its own set of attributes, which vary based on the Agency posting the docket. Another defining characteristic is if the docket is a Rulemaking or a Nonrulemaking Docket

### Searching for documents

You can search for a list of documents based on the criteria passed by using the endpoint `/v4/documents`. The search operation supports full text keyword searches and filtering based on a number of available parameters.

#### Detailed information for a single document

In order to obtain more details about a single document, you can use the endpoint `/v4/documents/{documentId}`. A document is defined by one of the following types: Proposed Rule, Rule, Supporting & Related, or Other. Each document type has its own set of attributes, which vary based on the Agency posting the document. Another defining characteristic is if the document is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

------

# `comments.py`

The `comments` python app fetches comments from the regulations.gov API related to quantum technology, computing, sensing, and communication.

`api_url = f"https://api.regulations.gov/v4/comments?filter[searchTerm]=quantum AND (technolog* OR information OR comput* OR sens* OR communication)&api_key={api_key}"`
