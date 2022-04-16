# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from matplotlib import image
from . import rec_sys
from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


ALLOWED_USECASES = ['gaming', 'work_business', 'home_personal']
ALLOWED_BRANDS = ['acer', 'asus', 'dell', 'gigabyte', 'hp', 'hyundai', 'lenovo', 'microsoft', 'msi', 'razer', 'toshiba']


class ValidateLaptopForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_laptop_form"

    async def required_slots(
        self, 
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher", 
        tracker: "Tracker", 
        domain: "DomainDict"
    ) -> List[Text]:
        if (tracker.slots.get("is_usecase") in [False, None]) and (tracker.slots.get("is_brand") in [False, None]) and (tracker.slots.get("is_screen_size") in [False, None]):
            return domain_slots
        elif tracker.slots.get("is_usecase") == True and (tracker.slots.get("is_brand") in [False, None]) and (tracker.slots.get("is_screen_size") in [False, None]):
            return ['price', 'is_usecase', 'usecase', 'is_brand', 'is_screen_size']
        elif tracker.slots.get("is_usecase") == True and tracker.slots.get("is_brand") == True and (tracker.slots.get("is_screen_size") in [False, None]):
            return ['price', 'is_usecase', 'usecase', 'is_brand', 'brand', 'is_screen_size']
        elif tracker.slots.get("is_usecase") == True and tracker.slots.get("is_brand") == False and tracker.slots.get("is_screen_size") == True:
            return ['price', 'is_usecase', 'usecase', 'is_brand', 'is_screen_size', 'screen_size']
        elif tracker.slots.get("is_usecase") == True and tracker.slots.get("is_brand") == True and tracker.slots.get("is_screen_size") == True:
            return ['price', 'is_usecase', 'usecase', 'is_brand', 'brand', 'is_screen_size', 'screen_size']    
        elif tracker.slots.get("is_usecase") == False and tracker.slots.get("is_brand") == True and (tracker.slots.get("is_screen_size") in [False, None]):
            return ['price', 'is_usecase', 'is_brand', 'brand', 'is_screen_size']
        elif tracker.slots.get("is_usecase") == False and tracker.slots.get("is_brand") == False and tracker.slots.get("is_screen_size") == True:
            return ['price', 'is_usecase', 'is_brand', 'is_screen_size', 'screen_size']
        elif tracker.slots.get("is_usecase") == False and tracker.slots.get("is_brand") == True and tracker.slots.get("is_screen_size") == True:
            return ['price', 'is_usecase', 'is_brand', 'brand', 'is_screen_size', 'screen_size']

    def validate_price(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if int(slot_value) < 20000 or int(slot_value) > 1300000:
            dispatcher.utter_message(text=f"Enter price between 20000 and 1300000 in rupees. for e.g. 50000")
            return {"price": None}
        dispatcher.utter_message(text=f"So you want a laptop of around {slot_value}.")
        return {"price": slot_value}

    def validate_usecase(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value.lower() not in ALLOWED_USECASES:
            dispatcher.utter_message(text=f"Please enter a valid laptop usecase.")
            return {"usecase": None}
        dispatcher.utter_message(text=f"Ok! Got your required usecase!")
        return {"usecase": slot_value}

    def validate_brand(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value.lower() not in ALLOWED_BRANDS:
            dispatcher.utter_message(text=f"I don't recognise that brand. I have {'/'.join(ALLOWED_BRANDS)} brands in my database.")
            return {"brand": None}
        dispatcher.utter_message(text=f"Ok! You want a laptop of brand {slot_value}.")
        return {"brand": slot_value}

# class ActionRec(Action):
#     def name(self):
#         return 'action_rec'

#     def run(self, dispatcher, tracker, domain):
#         rec_sys.get_rec(price=int(tracker.get_slot("price")), usecase=tracker.get_slot("usecase"), brand=tracker.get_slot("brand"), screen_size_name=tracker.get_slot("screen_size"))
#         dispatcher.utter_message(image="D:/new/ayush/rasa_beginner/actions/img/lap_rec.png")

#         return []    

class ActionRec(Action):
    def name(self):
        return 'action_rec'

    def run(self, dispatcher, tracker, domain):
        #out = rec_sys.get_rec(price=int(tracker.get_slot("price")), usecase=tracker.get_slot("usecase").lower(), brand=tracker.get_slot("brand").lower(), screen_size_name=tracker.get_slot("screen_size"))
        out = rec_sys.get_rec(price=int(tracker.get_slot("price")), usecase=tracker.get_slot("usecase"), brand=tracker.get_slot("brand"), screen_size_name=tracker.get_slot("screen_size"))
        #dispatcher.utter_message(image="C:/Users/Aayush Adhikari/_directory/rasa_beginner/actions/img/lap_rec.png")

        dispatcher.utter_message(text="Here are your suggestions")
        for i in range(len(out)):
            dispatcher.utter_message(text="{vari}".format(vari=json.dumps(out[i]).replace(r'{', '').replace('"', '').replace(r'}', '')))
        return []
