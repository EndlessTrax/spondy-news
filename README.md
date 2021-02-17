![GitHub](https://img.shields.io/github/license/endlesstrax/spondy-news)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)


![Spondy News](/static/imgs/logo.png)

# Spondy News

All the latest news, research, and events for those suffering with Axial Spondyloarthritis (axSpA).

## What is axSpA

It is a chronic inflammatory disease that includes radiographic (Ankylosing Spondylitis) and non-radiographic (nr-axSpA) forms. It is a rheumatic inflammatory disease primarily affecting the spine and sacroiliac joints. 

You can learn more about Ankylosing Spondylitis specifically [on my blog](https://endlesstrax.com/spondylitis/). And more about the general class of diseases on [spondylitis.org](https://spondylitis.org/about-spondylitis/types-of-spondylitis/).

## How to contribute

Spondy News is an open-source project, and as such, any help in improving user experience is appreciated. A few things to consider if you'd like to contribute:

- Before sumitting a PR, please raise and issue so that solutions or the problem can be discussed. This often leads to less time being spend on back-and-forth amending code and increases the chances of your PR being merged. 
- Please DO NOT submit PRs on the `main` branch. Once you've discussed your issue and forked the repo, create a branch specifically for your PR. 
- If you wouldn't use the language in front of your Grandmother, do use it in PRs and issues. Please keep comments respoectable. 
- If you have any questions at any point, add it to the issue, or reach our to me on [Twitter](https://twitter.com/endlesstrax).
- All code should be formatted with `Black` before submitting. 
- Ensure tests remain passing before you submit your PR. If any logic is added, ensure corresponding unit test/s are also included in your PR. 

## Setting up the project

Once forked, create yourself a **virtual environment** and `pip install` the dependancies from `requirements-dev.txt` file. The project uses **Python 3.9** _(recommended)_, but any version of Python that Django 3.1 supports _should_ work.

Secrets for this application are stored in environment variables. For local development you should create a `.env` file containing the `SECRET_KEY` and optionally, `DEBUG`.

```shell
# create a new random secret key
$ python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# create your .env file
$ touch spondy_news/.env
```

```
# In spondy_news/.env

SECRET_KEY=mynewsecretkey  # note: there are no quotes
DEBUG=True
```

Once dependancies are installed and you have your `.env` setup, run the Django migrations and create a superuser account:

```shell
$ python manage.py migrate
$ python manage.py migrate aggregator
$ python manage.py createsuperuser  # Then follow instructions
```

This app uses `whitenoise` to serve static files, so be sure to run `python manage.py collectstatic` before you start the server.

Start the server with `python manage.py runserver`. You should be now able to navigate to `127.0.0.1:8000` to see the site. The Django admin can be found at `admin/`.

This project uses a **custom django command** to run RSS feed parsing jobs on a schedule. These are **blocking** tasks and it needs to be run in a seperate process (terminal window). You can register the jobs and start the scheduling process in a seperate terminal:

```
$ python manage.py startjobs
```

These jobs can also be ran manually from the Django admin, once registered.

### Runing tests

`pytest` is the testing framework chosen for this project. It is included as a dev dependancy, so to run the test suite all you need to do is run:

```shell
$ pytest
```

That's it!

## Supporting this project

If you would like to show your support for the project using your wallet/purse, I would be very grateful if you would donate to a charity close to my heart, [Walk AS One](https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=DNSV3TV2SRLC2&source=url).

And if you would prefer to donate to me personally instead, you can [sponsor me on Github](https://github.com/sponsors/EndlessTrax) or [buy me a Ko-Fi](https://ko-fi.com/endlesstrax)? 🤓

Cheers!
