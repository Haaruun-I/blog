This is a hugo blog that uses the github graphql api to get the contents.
The `scripts` folder has a python script that handles the retreval and convertion of the gihtub data to a format hugo can accept, the rest of the folder structure is a standard hugo project, with a makefile and netlify configurations.

Current Features
- A project tab useing the pinned repositories of an account the repository names, descriptions, and readme files to create a page for each projects,
- An author blurb made from the profile readme. 
- Light and Dark Modes

Planned Additions
- A blog section, that uses an obsidian vault repository.
- Improved templates
- Custom python ssg, hugo feels too limmiting in format, and the convertion process is cumbersome
