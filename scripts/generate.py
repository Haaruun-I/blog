import requests, os, dotenv, content, pprint

dotenv.load_dotenv()

basePath = "./content/"
token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GITHUB_USERNAME')

print(username)
url = "https://api.github.com/graphql"

pinnedItemsQuery = """{
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

authorBlurbQuery = """{
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
    response = requests.post(url=url, json={"query": query}, headers= \
      {
        "Authorization": "Bearer %s" % token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/124.0"
      })
    return (response.json(), response.status_code)


authorBlurbResponse = graphqlQueary(url, token, authorBlurbQuery) \
                        [0]['data']['user']['repository']['object']['text']


root = content.Category("content", {
    'title': "Home"
},authorBlurbResponse)

posts = content.Category("posts", {'title': 'Posts'})
projects = content.Category("projects", {'title': 'Projects'})

root.children.append(posts)
root.children.append(projects)

pinnedItemsResponse = graphqlQueary(url, token, pinnedItemsQuery)
pinnedItemsResponse = pinnedItemsResponse[0]['data']['user']['pinnedItems']['nodes']

for repository in pinnedItemsResponse:
    article = content.Article(frontmatter = {
        'title': repository['name'],
        'date': repository['updatedAt'],
        'summary': repository['description'],
        'params: \n    ghLink': 'https://github.com/' + username + '/' + repository['name']
    }, body = repository['object']['text'])
    projects.children.append(article)

root.save()