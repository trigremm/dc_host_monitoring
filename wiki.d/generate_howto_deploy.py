# wiki.d/generate_howto_deploy.py
import argparse

from loguru import logger

RUN_SAMPLE = """
python generate_howto_deploy.py -w www.example.com -r https://github.com/trigremm/dc_host_monitoring
"""

HOWTO_TEMPLATE = """
# prepare for deploy snippet
# project_name: {project_name}
# repo_url    :     {repo_url} 
# git_url     :     {git_url}
# short_domain: {short_domain}
# www_domain  : {www_domain}

# generate ssh key in server for gitlab
ssh-keygen -b 2048 -t rsa -f ~/.ssh/deploy_key_{project_name} -C deploy_key_{project_name} -q -N ""

# add ssh key to gitlab deploy keys
cat ~/.ssh/deploy_key_{project_name}.pub
# gitlab case
# {repo_url}/-/settings/repository#js-deploy-keys-settings
# github case
# {repo_url}/settings/keys/new

# clone and add deploy key
GIT_SSH_COMMAND='ssh -i ~/.ssh/deploy_key_{project_name}' git clone {git_url}
cd {project_name}
git config core.sshCommand "ssh -i ~/.ssh/deploy_key_{project_name} -F /dev/null"

### deploy 
make r 

# add site config to nginx
rm -rf /etc/nginx/sites-available/{www_domain} /etc/nginx/sites-enabled/{www_domain}
ls -alsht conf.d/{www_domain}
cp conf.d/{www_domain} /etc/nginx/sites-available/{www_domain}
ln -s /etc/nginx/sites-available/{www_domain} /etc/nginx/sites-enabled/{www_domain}
nginx -t && nginx -s reload

# add site config to certbot
certbot --nginx -d {www_domain} -d {short_domain}
nginx -t && nginx -s reload

# make sure that the certificates are installed otherwise cloudflare will show host error page

#  brute force
systemctl restart nginx

"""


def validate_domain(www_domain):
    if not www_domain.startswith("www."):
        raise argparse.ArgumentTypeError("Domain must start with 'www.'")


def validate_repo_url(repo_url):
    if not repo_url.startswith("https://gitlab.com/") and not repo_url.startswith("https://github.com/"):
        raise argparse.ArgumentTypeError("Repo URL must start with 'https://gitlab.com/'")


def parse_args():
    parser = argparse.ArgumentParser(description="Process a domain and a Git URL.")

    parser.add_argument("-w", "--www_domain", help="The domain, must start with 'www.'")
    parser.add_argument("-r", "--repo_url", help="The Repo URL")

    args = parser.parse_args()

    return args.www_domain, args.repo_url


def main():
    www_domain, repo_url = parse_args()
    logger.info(f"{(www_domain, repo_url)=}")
    if not repo_url:
        print(RUN_SAMPLE)
        return

    validate_domain(www_domain)
    validate_repo_url(repo_url)

    short_domain = www_domain[4:]
    project_name = repo_url.strip("/").split("/")[-1]
    if "gitlab" in repo_url:
        git_url = repo_url.replace("https://gitlab.com/", "git@gitlab.com:") + ".git"
    elif "github" in repo_url:
        git_url = repo_url.replace("https://github.com/", "git@github.com:") + ".git"

    template = HOWTO_TEMPLATE.format(
        www_domain=www_domain,
        repo_url=repo_url,
        short_domain=short_domain,
        project_name=project_name,
        git_url=git_url,
    )

    with open("howto.txt", "w") as f:
        f.write(template)

    print("howto.txt generated")


if __name__ == "__main__":
    main()
