from rest_framework import serializers
import requests
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

class ReconSiteSerializer(serializers.Serializer) :
    url = serializers.CharField(max_length=512)

    def validate_url(self , value):

        main_url = value if value.startswith('http') else f'http://{value}'
        try:
            request = requests.get(main_url)
            return main_url
        except Exception as e:
            raise serializers.ValidationError('Can not access to this url')