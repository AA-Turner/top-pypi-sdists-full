cd ..

source .env

git remote remove divarteam_github_1
git remote add divarteam_github_1 git@github.com:divarteam/${project_name}.git

git remote -v