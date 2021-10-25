from pydantic import BaseModel, validator


class Configuration(BaseModel):
    service: str
    city: str

    @validator("service")
    def must_be_in(cls, value):
        if value.lower() not in ['open-street-map', 'google-map', 'bing']:
            raise ValueError("Available values are 'open-street-map', 'google-map', or 'bing.")
        return value.lower()
