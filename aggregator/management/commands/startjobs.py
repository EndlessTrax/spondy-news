# Standard Lib
import re
import logging
from datetime import timedelta

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Django
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

# Apps
from aggregator.models import Entry


logger = logging.getLogger(__name__)

GOOGLE_ALERT_FEEDS = {
    "axspa": "https://www.google.com/alerts/feeds/12301481115898191089/13630488004246171818",
    "spondylitis": "https://www.google.com/alerts/feeds/12301481115898191089/5579286489481723714",
    "spondyloarthritis": "https://www.google.com/alerts/feeds/12301481115898191089/5989929665899114034",
    "spondyloarthropathy": "https://www.google.com/alerts/feeds/12301481115898191089/3186404085116501193",
}

PUBMED_FEEDS = {
    "axial spondyloarthritis": "https://pubmed.ncbi.nlm.nih.gov/rss/search/14CrWYUMC68Kd_QhNo0LutvubuiZrdL47utc2tIJJ8pCWGNMyR/?limit=20&utm_campaign=pubmed-2&fc=20210117223700",
    "ankylosing spondylitis": "https://pubmed.ncbi.nlm.nih.gov/rss/search/1pabLar0q26GwV21NSLZ__LYXTO1Ur5WgUsuRUtJ8aJnHsugMd/?limit=20&utm_campaign=pubmed-2&fc=20210117223855",
}

AS_NEWS_DOTCOM_FEED = "https://ankylosingspondylitisnews.com/feed/"


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def remove_html_elements(string: str) -> str:
    """Removes any html elements and attributes from any string passed"""
    regex = re.compile("<.*?>")
    clean_text = re.sub(regex, "", string)
    return clean_text


def parse_google_alert_feed(url: str) -> None:
    """Parsing function for all Google Alert RSS feeds.

    All entries gathered from these feeds are aytomatically give the ARTICLE
    category.
    """
    feed = feedparser.parse(url)
    try:
        for item in feed.entries:
            if not Entry.objects.filter(link=item.link).exists():
                entry = Entry(
                    title=remove_html_elements(item.title),
                    description=remove_html_elements(item.content[0]["value"]),
                    pub_date=parser.parse(item.updated),
                    link=item.link,
                    category="ARTICLE",
                )
                entry.save()
    except:
        logger.warn("No items in the Feed")


def parse_pubmed_feed(url: str) -> None:
    """Parsing function for all PubMed RSS feeds.

    All entires gathered from these feeds are aytomatically give the RESEARCH
    category.
    """
    feed = feedparser.parse(url)
    try:
        for item in feed.entries:
            # Pubmed uses query strings in its RSS feeds which leads to
            # multiple duplicates when items appear on more than one feed.
            # Therefore, pubmed feeds we use the title as the unique identifier
            if not Entry.objects.filter(title=item.title).exists():
                entry = Entry(
                    title=remove_html_elements(item.title),
                    description=remove_html_elements(item.description),
                    pub_date=parser.parse(item.published),
                    link=item.link,
                    category="RESEARCH",
                )
                entry.save()
    except:
        logger.warn("No items in the Feed")


def delete_rejected_entries() -> None:
    """Deletes old entries that were not marked is_published and used"""
    start_range = timezone.now() - timedelta(days=365)
    end_range = timezone.now() - timedelta(days=14)
    to_be_deleted = Entry.objects.filter(is_published=False, pub_date__range=[start_range, end_range])

    for entry in to_be_deleted:
        try:
            entry.delete()
            logger.info(f"Deleted entry: {entry.title}")
        except:
            logger.info(f"Unable to delete entry: {entry.title}")


def axspa_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing axspa feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["axspa"])


def spondylitis_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing spondylitis feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondylitis"])


def spondyloarthritis_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing spondyloarthritis feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondyloarthritis"])


def spondyloarthropathy_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing spondyloarthropathy feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondyloarthropathy"])


def research_axspa_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing axial spondyloarthritis PUBMED feed...")
    parse_pubmed_feed(PUBMED_FEEDS["axial spondyloarthritis"])


def research_as_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing ankylosing spondylitis PUBMED feed...")
    parse_pubmed_feed(PUBMED_FEEDS["ankylosing spondylitis"])


def as_news_dotcom_feed() -> None:
    """Function to be passed to a Django-APScheduler job"""
    logger.info("Parsing AnkylosingSpondylitisNews.com feed...")
    parse_pubmed_feed(AS_NEWS_DOTCOM_FEED)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            axspa_feed,
            trigger="interval",
            hours=12,
            minutes=30,
            id="Keyword: axspa",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: axspa_feed")

        scheduler.add_job(
            spondylitis_feed,
            trigger="interval",
            hours=12,
            id="Keyword: spondylitis",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondylitis_feed")

        scheduler.add_job(
            spondyloarthritis_feed,
            trigger="interval",
            hours=12,
            minutes=10,
            id="Keyword: spondyloarthritis",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondyloarthritis_feed")

        scheduler.add_job(
            spondyloarthropathy_feed,
            trigger="interval",
            hours=12,
            minutes=20,
            id="Keyword: spondyloarthropathy",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondyloarthropathy_feed")

        scheduler.add_job(
            research_axspa_feed,
            trigger="interval",
            hours=6,
            id="Research: AxSpa",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: research_axspa_feed")

        scheduler.add_job(
            research_as_feed,
            trigger="interval",
            hours=6,
            minutes=10,
            id="Research: AS",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: research_as_feed")

        scheduler.add_job(
            as_news_dotcom_feed,
            trigger="interval",
            hours=6,
            id="AS News dotcom feed",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: as_news_dotcom_feed")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete old job executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: delete_old_job_executions")

        scheduler.add_job(
            delete_rejected_entries,
            trigger=CronTrigger(day_of_week="mon", hour="01", minute="00"),
            id="delete old rejected entries",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: delete_rejected_entries")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
