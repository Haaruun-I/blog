import requests, os, dotenv

dotenv.load_dotenv()

basePath = "./page_gen"
url = "https://api.github.com/graphql"
token = os.getenv('GITHUB_TOKEN')
query = """{
  user(login: "DevonCrawford") {
    pinnedItems(first: 10, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          updatedAt
          object(expression: "master:README.md") {
            ... on Blob {
              text
            }
          }
        }
      }
    }
  }
}"""

def graphqlQueary(url, token, query):
    response = requests.post(url=url, json={"query": query}, headers={"Authorization": "token %s" % token})
    return (response.json(), response.status_code)

def formatFile(repository):
    return """---
title: %s
date: %s
summary: %s
---
%s""" % (repository['name'], repository['updatedAt'], repository['description'], repository['object']['text'] if repository['object'] else "")

repositories = graphqlQueary(url, token, query)[0]['data']['user']['pinnedItems']['nodes']
for repository in repositories:
    name = "%s/%s.md" % (basePath, repository['name'])
    body = formatFile(repository)
    with open(name, 'w') as file:
        file.write(body)
