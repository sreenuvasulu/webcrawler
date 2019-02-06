from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE
from BeautifulSoup import BeautifulSoup
import urllib2


class GetSiteInfo(ListAPIView):
    """
        Sample Request Url = http://127.0.0.1:8000/get_site_info/?link=https://cloudscene.com/
        Response = {
                        "message": "we got some result",
                        "data": {
                                "requested_url":"",
                                "links": [
                                            {
                                                "images": [

                                                ],
                                                "link": ""
                                            }
                                        ]
                                }
                    }

    """
    url = None
    avoid_links = ['facebook.com', 'twitter.com']

    def get_soup_code(self, url):
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page)
        return soup

    def get_links(self):
        links_list = list()
        soup = self.get_soup_code(self.url)
        for link in soup.findAll('a', href=True):
            append_link = link.get('href')
            if append_link and all([True if aviod_link not in append_link.lower() else False
                                    for aviod_link in self.avoid_links]):
                links_list.append(append_link)
        return list(set(links_list))

    def get_images(self, url):
        images_list = list()
        soup = self.get_soup_code(url)
        for link in soup.findAll('img', src=True):
            image = link.get('src')
            if image and all([True if aviod_link not in image.lower() else False for aviod_link in self.avoid_links]):
                images_list.append(image)
        return list(set(images_list))

    def get(self, request, *args, **kwargs):
        self.url = request.GET.get('link')
        main_data = dict()
        main_data["requested_url"] = self.url
        main_data["links"] = []
        response = {"message": ""}
        status = HTTP_200_OK
        if self.url is None or not all([True for aviod_link in self.avoid_links if aviod_link not in self.url.lower()]):
            response["message"] = "Wrong url Received."
            status = HTTP_406_NOT_ACCEPTABLE
        else:
            links = self.get_links()
            for link_url in links:
                obj = dict()
                obj["link"] = link_url
                obj["images"] = self.get_images(link_url)
                main_data["links"].append(obj)
            response["message"] = "we got some result"
            response["data"] = main_data
        return Response(response, status=status)


