# Standard Lib
import re
import logging

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
from content_aggregator.models import Entry


logger = logging.getLogger(__name__)

GOOGLE_ALERT_FEEDS = {
    "axspa": "https://www.google.com/alerts/feeds/12301481115898191089/5318901876884769878",
    "spondylitis": "https://www.google.com/alerts/feeds/12301481115898191089/134735491328814164",
    "spondyloarthritis": "https://www.google.com/alerts/feeds/12301481115898191089/7707450025187624950",
    "spondyloarthropathy": "https://www.google.com/alerts/feeds/12301481115898191089/12414979335294108273",
}


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def remove_html_elements(string: str) -> str:
    regex = re.compile("<.*?>")
    clean_text = re.sub(regex, "", string)
    return clean_text


def parse_google_alert_feed(url):
    feed = feedparser.parse(url)
    try:
        for item in feed.entries:
            if not Entry.objects.filter(link=item.link).exists():
                entry = Entry(
                    title=remove_html_elements(item.title),
                    description=remove_html_elements(item.content[0]["value"]),
                    pub_date=parser.parse(item.updated),
                    link=item.link,
                )
                entry.save()
    except:
        logger.warn("No items in the Feed")


def axspa_feed():
    logger.info("Parsing axspa feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["axspa"])


def spondylitis_feed():
    logger.info("Parsing spondylitis feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondylitis"])


def spondyloarthritis_feed():
    logger.info("Parsing spondyloarthritis feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondyloarthritis"])


def spondyloarthropathy_feed():
    logger.info("Parsing spondyloarthropathy feed...")
    parse_google_alert_feed(GOOGLE_ALERT_FEEDS["spondyloarthropathy"])


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            axspa_feed,
            trigger="interval",
            hours=6,
            id="Keyword: axspa",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: axspa_feed")

        scheduler.add_job(
            spondylitis_feed,
            trigger="interval",
            hours=2,
            id="Keyword: spondylitis",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondylitis_feed")

        scheduler.add_job(
            spondyloarthritis_feed,
            trigger="interval",
            hours=2,
            minutes=10,
            id="Keyword: spondyloarthritis",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondyloarthritis_feed")

        scheduler.add_job(
            spondyloarthropathy_feed,
            trigger="interval",
            hours=2,
            minutes=20,
            id="Keyword: spondyloarthropathy",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: spondyloarthropathy_feed")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: delete_old_job_executions")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
