import requests, os, dotenv

dotenv.load_dotenv()

basePath = "./content/"
url = "https://api.github.com/graphql"
token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GITHUB_USERNAME')

query = """{
  user(login: "%s") {
    pinnedItems(first: 10, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          updatedAt
          object(expression: "HEAD:README.md") {
            ... on Blob {
              text
            }
          }
        }
      }
    }
  }
}""" % username

authorBlurb = """{
      user(login: "%s") {
        repository(name: "%s") {
            object(expression: "HEAD:README.md") {
                ... on Blob {
                    text
                }
            }
        }
    }
}""" % (username, username.lower())

def graphqlQueary(url, token, query):
    response = requests.post(url=url, json={"query": query}, headers={"Authorization": "token %s" % token})
    return (response.json(), response.status_code)

def formatFile(metadata, body):
    filetext = "---"
    for key in metadata.keys():
        filetext += '\n%s: %s' % (key, metadata[key])
    filetext += '\n---\n%s' % body
    return filetext

def writeFile(name, body):
    with open(name, 'w') as file:
        file.write(body)

response = graphqlQueary(url, token, query)
repositories = response[0]['data']['user']['pinnedItems']['nodes']
for repository in repositories:
    body = formatFile({
        'title': repository['name'],
        'date': repository['updatedAt'],
        'summary': repository['description']
    }, repository['object']['text'])
    writeFile(basePath + "projects/" + repository['name'] + '.md', body)

response = graphqlQueary(url, token, authorBlurb)
readme = response[0]['data']['user']['repository']['object']['text']
writeFile(basePath + "_index.md", formatFile({'title': 'Home'}, readme))
