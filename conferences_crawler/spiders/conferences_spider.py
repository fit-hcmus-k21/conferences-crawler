import scrapy


roles = [
    "Application & Software Engineering",
    "CIOs & IT Executives",
    "Data & Analytics",
    "IT Infrastructure & Operations",
    "Security & Risk Management",
    "Technology & Service Providers",
]

class Item:
    title = scrapy.Field()
    start_date = scrapy.Field()
    location = scrapy.Field()
    topic = scrapy.Field()
    region = scrapy.Field()
    url = scrapy.Field()
    speakers = scrapy.Field()
    timeline = scrapy.Field()
    register_url = scrapy.Field()
    track = scrapy.Field()

class ConferencesSpider(scrapy.Spider):
    name = "conferences"
    start_urls = [
        "https://www.gartner.com/en/conferences/calendar",
    ]

    def parse(self, response):
        for conf in response.css("div.conference-tile a"):
            role = conf.xpath("@data-primary-role").get()
        
            if (role in roles):
                item = Item()
                url = response.urljoin(conf.xpath("@href").get())
                item.title = conf.xpath("@data-gtm-title").get()
                item.start_date = conf.xpath("@data-gtm-start-date").get()
                item.location = conf.xpath("@data-gtm-location").get()
                item.topic = role
                item.region = conf.xpath("@data-region").get()
                item.url = url

                yield response.follow(url + "/speakers", self.parse_conf, meta={'item': item})

    def parse_conf(self, response):
        item = response.meta['item']

        item.register_url = item.url + "/register"

        first_featured_container = response.css("div.featured-container")[0]
        speakers = first_featured_container.css("div.member")
        list_speakers = []
        for speaker in speakers:
            name = speaker.css("div.headline h4::text").get()
            major = speaker.css("div.jobTitle::text").get()
            bio_detail = item.url + speaker.xpath("a /@href").get()

            list_speakers.append({"name": name, "major": major, "bio_detail": bio_detail})

        item.speakers = list_speakers

        yield response.follow(item.url + "/agenda/day", self.parse_agenda, meta={'item': item})


    def parse_agenda(self, response):
        item = response.meta['item']
        agenda_days = []
        link_detail = response.url
        days_panel = response.css("div.agenda-panel-heading")
        for day in days_panel:
            day_detail = day.css("a h2::text").get()
            agenda_days.append({"day": day_detail})

        item.timeline = {
            "link_detail": link_detail,
            "agenda_days": agenda_days
        }

        yield response.follow(item.url + "/agenda", self.parse_tracks, meta={'item': item})

    
    def parse_tracks(self, response):
        item = response.meta['item']

        list_tracks = []

        tracks_panel = response.css("div.agenda-panel-heading")
        for track in tracks_panel:
            track_title = track.css("a h2::text").get()
            list_tracks.append({"track_title": track_title})

        item.track = list_tracks
            

        yield {
            "name": item.title,
            "start_date": item.start_date,
            "location": item.location,
            "topic": item.topic,
            "region": item.region,
            "url": item.url,
            "speakers": item.speakers,
            "timeline": item.timeline,
            "track": item.track,
            "register_url": item.register_url,
        }

        


        