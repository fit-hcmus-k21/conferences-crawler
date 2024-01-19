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
    agenda = scrapy.Field()

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
        first_featured_container = response.css("div.featured-container").get()
        speakers = first_featured_container.xpath("div[@class='speaker']")
        list_speakers = []
        for speaker in speakers:
            name = speaker.css("div.headline h4::text").get()
            major = speaker.css("div.jobTitle::text").get()
            list_speakers.append({"name": name, "major": major})

        item.speakers = first_featured_container

        yield response.follow(item.url + "/agenda/day", self.parse_agenda, meta={'item': item})


    def parse_agenda(self, response):
        item = response.meta['item']
        agenda_days = []
        days_panel = response.xpath("//div[@class='panel']")
        for day in days_panel:
            day_detail = day.xpath("div[@class='agenda-panel-heading-text']/h2/text()").get()
            link_detail = day.xpath("div[@class='panel-heading']/@href").get()
            agenda_days.append({"day": day_detail, "link": link_detail})

        item.agenda = days_panel
            
        yield {
            "name": item.title,
            "start_date": item.start_date,
            "location": item.location,
            "topic": item.topic,
            "region": item.region,
            "url": item.url,
            "speakers": item.speakers,
            "agenda": item.agenda
        }

        


        