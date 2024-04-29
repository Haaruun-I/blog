This is a hugo site for my blog and portfolio page. 

The `project` collection holds all the projects you want to show off. It works by pulling from the Github API and getting all the pinned repositories on an account, and taking the README file, project discription, and homepage, and using it to generate a page for each.

The `author blurb` section is taken from the profile readme repository on github.

The `posts` collection is for any articles. It takes a git repository containting a obsidian vault, and uses [Obsidian-to-hugo](https://github.com/devidw/obsidian-to-hugo) to convert the contents to something hugo can take as input. 

This site is hosted on netlify, and uses the github webhooks to automate redeployment on new releases from the refrenced repositories.

Glitch animation inspired by [CSS Tricks](https://css-tricks.com/glitch-effect-text-images-svg/)

Planned Additions
- Improved templates
- Custom python ssg, hugo feels too limmiting in format, and the convertion process is cumbersome
