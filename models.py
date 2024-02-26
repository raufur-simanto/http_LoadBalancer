import requests


class Server:
    def __init__(self, endpoint, path='/healthcheck'):
        self.endpoint = endpoint
        self.path = path
        self.healthy = True
        self.timeout = 1
        self.protocol = 'http://'
    
    def healthcheck_and_update_status(self):
        # print("get in")
        try:
            response = requests.get(f"{self.protocol}{self.endpoint}{self.path}", timeout=self.timeout)
            print(f"Response: {response}")

            if response.ok:
                self.healthy = True
            else:
                self.healthy = False
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.healthy = False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Server):
            return self.endpoint == other.endpoint
        return False
    
    def __repr__(self) -> str:
        return f"<Server: {self.endpoint} {self.healthy} {self.timeout}>"
    

