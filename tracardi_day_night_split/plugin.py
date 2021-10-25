import re
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

from tracardi_day_night_split.model.configuration import Configuration
from tracardi_day_night_split.service.day_night_checker import is_day


def validate(config: dict):
    return Configuration(**config)


class DayNightSplitAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        city = dot[self.config.city]

        if is_day(city, self.config.service):
            return Result(value=payload, port="day"), Result(value=None, port="night")

        return Result(value=None, port="day"), Result(value=payload, port="night")


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_day_night_split.plugin',
            className='DayNightSplitAction',
            inputs=['payload'],
            outputs=["day", "night"],
            manual='day_night_split_action',
            init={
                "service": "open-street-map",
                "city": "paris"
            },
            version="0.6.0",
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="service",
                            name="Geo location service provider",
                            description="Select service provider.",
                            component=FormComponent(type="select", props={
                                "label": "provider",
                                "items": {
                                    "open-street-map": "Open Street Map",
                                    "google-map": "Google Map",
                                    "bing": "Bing"
                                }})
                        ),
                        FormField(
                            id="city",
                            name="City",
                            description="Path to city data or city itself.",
                            component=FormComponent(type="dotPath", props={"label": "City"})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='City Day/Night',
            desc='Splits workflow whether it is day or night in a given city.',
            type='flowNode',
            width=200,
            height=100,
            icon='dark-light',
            group=["Time"]
        )
    )
