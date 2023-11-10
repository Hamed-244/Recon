from rest_framework import serializers
import requests


class ReconSiteSerializer(serializers.Serializer) :
    url = serializers.CharField(max_length=512)

    def validate_url(self , value):
        try :
            check_url = requests.get(value if value.startswith('http') else f'http://{value}')
            if check_url.status_code == 200 :
                return value
            raise serializers.ValidationError('Can not access to this url')
        except Exception as error:
            print(error)
            raise serializers.ValidationError('Invalid url please enter a valid url')