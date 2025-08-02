cd ..

source .env

git remote remove arpakit_github_1
git remote add arpakit_github_1 git@github.com:arpakit/${project_name}.git

git remote remove arpakit_gitlab_1
git remote add arpakit_gitlab_1 git@gitlab.com:arpakit/${project_name}.git

git remote -v
