import os

def writeFile(name, body):
    with open(name, 'w') as file:
        file.write(body)

def writeFile(name, body):
    with open(name, 'w') as file:
        file.write(body)

class Article():
    def __init__(self, name="", frontmatter={}, body=""):
        self.frontmatter = frontmatter
        self.body = body

    def formatFile(self):
        filetext = "---"
        for key in self.frontmatter.keys():
            filetext += '\n%s: %s' % (key, self.frontmatter[key])
        filetext += '\n---\n%s' % self.body
        return filetext

    def __str__(self):
        return self.formatFile()

class Category():
    def __init__(self, name="", frontmatter={}, body=""):
        self.name = name
        self.frontmatter = frontmatter
        self.children = []
        self.body = body

    def formatFile(self):
        filetext = "---"
        for key in self.frontmatter.keys():
            print(key)
            filetext += '\n%s: %s' % (key, self.frontmatter[key])
        filetext += '\n---\n%s' % self.body
        return filetext

    def save(self, parent_folder="."):
        folder_path = os.path.join(parent_folder, self.name)
        os.makedirs(folder_path, exist_ok=True)


        index_content = self.formatFile()
        index_file_path = os.path.join(folder_path, "_index.md")
        writeFile(index_file_path, index_content)

        print('test')
        for child in self.children:
            print(child)
            if isinstance(child, Article):
                child_file_path = os.path.join(folder_path, f"{child.frontmatter['title']}.md")
                writeFile(child_file_path, child.formatFile())

            elif isinstance(child, Category):
                child.save(folder_path)