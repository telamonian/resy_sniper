from requests import get, post

class ResyApi:
    def __init__(self, api_key, auth_token):
        self.api_key = api_key
        self.auth_token = auth_token

        self.baseUrl = "https://api.resy.com"

    @property
    def headers(self):
        return {
            "Authorization": f'ResyAPI api_key="{self.api_key}"',
            "x-resy-auth-token": self.auth_token,
        }

    def get(self, path, params):
        url = self.baseUrl + path

        req = get(url, headers=self.headers, params=params)
        return req.json()
    
    def post(self, path, params):
        url = self.baseUrl + path

        headers = {**self.headers, **{
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://widgets.resy.com",
            "Referer": "https://widgets.resy.com/",
        }}

        # the post body accepts params stringified a-la query parameters, for some reason
        body = "&".join(f"{k}={v}" for k,v in params.items())

        req = post(url, headers=headers, data=body)
        return req.json()

    def getReservations(self, date, partySize, venueId):
        params = {
            "lat":        "0",
            "long":       "0",
            "day":        date,
            "party_size": str(partySize),
            "venue_id":   str(venueId),
        }

        return self.get("/4/find", params)
        
    def getReservationDetails(self, configId, date, partySize):
        params = {
            "config_id":  configId,
            "day":        date,
            "party_size": partySize.toString
        }

        return self.get("/3/details", params)
    
    def getReservationDetails(self, paymentMethodId, bookToken):
        params = {
            "book_token":            bookToken,
            "struct_payment_method": f'{{"id":{paymentMethodId}}}',
        }

        return self.get("/3/book", params)
