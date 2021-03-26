from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import dbus
import json


class AwesomewmClientListExtension(Extension):

    def __init__(self):
        super(AwesomewmClientListExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        bus = dbus.SessionBus()
        obj = bus.get_object('org.awesomewm.awful', '/')
        self.interface = dbus.Interface(obj, 'org.awesomewm.awful.umbe')


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        search = str(event.get_argument() or '').lower().strip()
        items = []

        clientsString = extension.interface.client_list("{}")
        clients = json.loads(clientsString)
        for clt in clients:
            if search == '' or search in clt["class"].lower() or search in clt["name"]:
                data = (clt["wid"])
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=clt["class"],
                                                 description=clt["name"],
                                                 on_enter=ExtensionCustomAction(data)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        wid = event.get_data()
        client = {'wid': wid}
        extension.interface.activate_client(json.dumps(client))


if __name__ == '__main__':
    AwesomewmClientListExtension().run()
