import requests, os, dotenv, content, pprint

dotenv.load_dotenv()

basePath = "./content/"
token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GITHUB_USERNAME')

url = "https://api.github.com/graphql"

pinnedItemsQuery = """{
  user(login: "%s") {
    pinnedItems(first: 10, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          updatedAt
          homepageUrl
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

notfoundPage = content.Article(frontmatter={
  "title": "404 Not Found",
  "date": "None"
}, body="Sorry, the page your looking for cannot be found", filename="404.md")
root.children.append(notfoundPage)

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
        'homepage': repository['homepageUrl'],
        'projectPage': 'https://github.com/' + username + '/' + repository['name'], 
    }, body = repository['object']['text'])
    projects.children.append(article)

root.save()

os.system('git clone ' + os.getenv('BLOG_REPO') + " temp")

from obsidian_to_hugo import ObsidianToHugo
import subprocess

# TODO unspaget this code
def addFrontmatter(text, path):
    temp = text.split("---")
    print(len(temp))
    if len(temp) >= 2:
      summary = temp[0].lstrip()
      body = '---'.join(temp[1:])
    else:
      summary=""
      body=text
    date = subprocess.run(['cd temp && git log -1 --pretty="format:%ct" "' + path + '"'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(path +": " + str(date))
    t = str(content.Article(frontmatter = {
      'title': path.split('.')[0],
      'summary': summary,
      'date': str(date)
    }, body = body))
    print(t)
    return t

obsidian_to_hugo = ObsidianToHugo(
    obsidian_vault_dir="./temp",
    hugo_content_dir="./content/posts",
    processors=[addFrontmatter]
)

obsidian_to_hugo.run()