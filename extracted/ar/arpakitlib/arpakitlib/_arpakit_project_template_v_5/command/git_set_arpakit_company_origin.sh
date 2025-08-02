cd ..

source .env

git remote remove arpakit_company_github_1
git remote add arpakit_company_github_1 git@github.com:ARPAKIT-Company/${project_name}.git

git remote remove arpakit_company_gitlab_1
git remote add arpakit_company_gitlab_1 git@gitlab.com:ARPAKIT-Company/${project_name}.git

git remote -v