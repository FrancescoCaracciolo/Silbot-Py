"""
## In this module there is the botApi class, whose purpose is to send requests
"""

import requests
import json
from silbot import types, helper
from silbot.response import BotAPIResponse


class BotApi:
    """
    Class to send requests to botAPI
    """

    def __init__(self, token, default_parse_mode: str = None, default_disable_web_preview: bool = None,
                 default_disable_notifications: bool = None):
        """Creates a botApi by the given token

        Using this class you can easily send requests to botApi and use the response
        - - - - -
        **Args**:

        - `token` (`str`): bot's API Token given by [@botfather](https://t.me/botfather)
        - `default_parse_mode` (`str`, *optional*): Can be None, Markdown or HTML, it is used in functions if parse_mode is not specified. Defaults to `None`.
        - `default_disable_web_preview` (`bool`, *optional*): It is used in functions if disable_web_page_preview is not specified. Defaults to `None`.
        - `default_disable_notifications` (`bool`, *optional*): It is used in functions if disable_notifications is not specified. Defaults to `None`.
        """
        self.default_parse_mode = default_parse_mode
        self.default_disable_web_preview = default_disable_web_preview
        self.default_disable_notifications = default_disable_notifications

        self.token = token
        self.session = requests.Session()

    def sendRequest(self, method, arguments=None):
        """Sends a GET request to botAPI

        Using this function you can send custom requests to botAPI
        - - - - -
        **Args**:

        - `method` (`str`): request method, like sendMessage
        - `arguments` (`dict`, *optional*): A `dict` whose keys are request's parameters and the values are parameters values. Defaults to `{}`.

        **Returns**
        - `str` botAPI's string response
        """
        if arguments is None:
            arguments = {}
        try:
            r = self.session.get("https://api.telegram.org/bot" + self.token + "/" + method, params=arguments, timeout=10)
        except Exception:
            return json.dumps({"ok": False, "connection_error": True})
        else:
            return r.text

    @staticmethod
    def response(raw_json, func):
        """Creates a botAPIResponse object for the given JSON

        - - - - -
        **Args**:

        - `raw_json` (`str`): Result from botAPI
        - `func` (`silbot.types` class or builtin data value): Expected result from botAPI

        **Returns**
        - `tuple` containing the expected result as object as first argument and the `BotAPIResponse` object as second
        """
        response = BotAPIResponse(raw_json, func)
        return response.getObject(), response

    def getUpdates(self, offset: int = None, limit: int = None, timeout: int = None, allowed_updates: list = None):
        """Use this method to receive incoming updates using long polling (wiki). An Array of Update objects is returned. [See Telegram API](https://core.telegram.org/bots/api#getupdates)

        - - - - -
        **Args**:

        - `offset` :`int` Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will forgotten.
        - `limit` :`int` Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        - `timeout` :`int` Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
        - `allowed_updates` :`list` A JSON-serialized list of the update types you want your bot to receive. For example, specify ['message', 'edited_channel_post', 'callback_query'] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all updates regardless of type (default). If not specified, the previous setting will be used.Please note that this parameter doesn't affect updates created before the call to the getUpdates, so unwanted updates may be received for a short period of time.

        **Returns:**

        - A `tuple`, on success a `list` as first member and a botApiResponse object as second member
        """
        data = {
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates,
        }
        return self.response(self.sendRequest("getUpdates", data), list)

    def setWebhook(self, url: str, certificate: types.InputFile = None, max_connections: int = None, allowed_updates: list = None):
        """Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts. Returns True on success.
        If you'd like to make sure that the Webhook request comes from Telegram, we recommend using a secret path in the URL, e.g. https://www.example.com/<token>. Since nobody else knows your bot's token, you can be pretty sure it's us. [See Telegram API](https://core.telegram.org/bots/api#setwebhook)

        - - - - -
        **Args**:

        - `url` :`str` HTTPS url to send updates to. Use an empty string to remove webhook integration
        - `certificate` :`types.InputFile` Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        - `max_connections` :`int` Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        - `allowed_updates` :`list` A JSON-serialized list of the update types you want your bot to receive. For example, specify ['message', 'edited_channel_post', 'callback_query'] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all updates regardless of type (default). If not specified, the previous setting will be used.Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "url": url,
            "certificate": helper.toDict(certificate, True),
            "max_connections": max_connections,
            "allowed_updates": allowed_updates,
        }
        return self.response(self.sendRequest("setWebhook", data), bool)

    def deleteWebhook(self, ):
        """Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success. Requires no parameters. [See Telegram API](https://core.telegram.org/bots/api#deletewebhook)

        - - - - -
        **Args**:


        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
        }
        return self.response(self.sendRequest("deleteWebhook", data), bool)

    def getWebhookInfo(self, ):
        """Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty. [See Telegram API](https://core.telegram.org/bots/api#getwebhookinfo)

        - - - - -
        **Args**:


        **Returns:**

        - A `tuple`, on success a `types.WebhookInfo` as first member and a botApiResponse object as second member
        """
        data = {
        }
        return self.response(self.sendRequest("getWebhookInfo", data), types.WebhookInfo)

    def getMe(self, ):
        """A simple method for testing your bot's auth token. Requires no parameters. Returns basic information about the bot in form of a User object. [See Telegram API](https://core.telegram.org/bots/api#getme)

        - - - - -
        **Args**:


        **Returns:**

        - A `tuple`, on success a `types.User` as first member and a botApiResponse object as second member
        """
        data = {
        }
        return self.response(self.sendRequest("getMe", data), types.User)

    def sendMessage(self, chat_id: (int, str), text: str, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, disable_web_page_preview: bool = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send text messages. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendmessage)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `text` :`str` Text of the message to be sent, 1-4096 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the message text. See formatting options for more details.
        - `disable_web_page_preview` :`bool` Disables link previews for links in this message
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_web_page_preview is None:
            disable_web_page_preview = self.default_disable_web_preview

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendMessage", data), types.Message)

    def forwardMessage(self, chat_id: (int, str), message_id: int, from_chat_id: (int, str), disable_notification: bool = None):
        """Use this method to forward messages of any kind. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#forwardmessage)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Message identifier in the chat specified in from_chat_id
        - `from_chat_id` :`(int,str,)` Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "disable_notification": disable_notification,
            "message_id": message_id,
        }
        return self.response(self.sendRequest("forwardMessage", data), types.Message)

    def sendPhoto(self, chat_id: (int, str), photo: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send photos. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendphoto)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `photo` :`(types.InputFile,str,)` Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the photo caption. See formatting options for more details.
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "photo": helper.toDict(photo, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendPhoto", data), types.Message)

    def sendAudio(self, chat_id: (int, str), audio: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, duration: int = None, performer: str = None, title: str = None, thumb: (types.InputFile, str) = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        For sending voice messages, use the sendVoice method instead. [See Telegram API](https://core.telegram.org/bots/api#sendaudio)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `audio` :`(types.InputFile,str,)` Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Audio caption, 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the audio caption. See formatting options for more details.
        - `duration` :`int` Duration of the audio in seconds
        - `performer` :`str` Performer
        - `title` :`str` Track name
        - `thumb` :`(types.InputFile,str,)` Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://<file_attach_name>' if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files '
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "audio": helper.toDict(audio, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "duration": duration,
            "performer": performer,
            "title": title,
            "thumb": helper.toDict(thumb, True),
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendAudio", data), types.Message)

    def sendDocument(self, chat_id: (int, str), document: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, thumb: (types.InputFile, str) = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future. [See Telegram API](https://core.telegram.org/bots/api#senddocument)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `document` :`(types.InputFile,str,)` File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the document caption. See formatting options for more details.
        - `thumb` :`(types.InputFile,str,)` Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://<file_attach_name>' if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files '
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "document": helper.toDict(document, True),
            "thumb": helper.toDict(thumb, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendDocument", data), types.Message)

    def sendVideo(self, chat_id: (int, str), video: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, duration: int = None, width: int = None, height: int = None, thumb: (types.InputFile, str) = None, supports_streaming: bool = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future. [See Telegram API](https://core.telegram.org/bots/api#sendvideo)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `video` :`(types.InputFile,str,)` Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the video caption. See formatting options for more details.
        - `duration` :`int` Duration of sent video in seconds
        - `width` :`int` Video width
        - `height` :`int` Video height
        - `thumb` :`(types.InputFile,str,)` Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://<file_attach_name>' if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files '
        - `supports_streaming` :`bool` Pass True, if the uploaded video is suitable for streaming
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "video": helper.toDict(video, True),
            "duration": duration,
            "width": width,
            "height": height,
            "thumb": helper.toDict(thumb, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "supports_streaming": supports_streaming,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendVideo", data), types.Message)

    def sendAnimation(self, chat_id: (int, str), animation: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, duration: int = None, width: int = None, height: int = None, thumb: (types.InputFile, str) = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future. [See Telegram API](https://core.telegram.org/bots/api#sendanimation)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `animation` :`(types.InputFile,str,)` Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the animation caption. See formatting options for more details.
        - `duration` :`int` Duration of sent animation in seconds
        - `width` :`int` Animation width
        - `height` :`int` Animation height
        - `thumb` :`(types.InputFile,str,)` Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://<file_attach_name>' if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files '
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "animation": helper.toDict(animation, True),
            "duration": duration,
            "width": width,
            "height": height,
            "thumb": helper.toDict(thumb, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendAnimation", data), types.Message)

    def sendVoice(self, chat_id: (int, str), voice: (types.InputFile, str), caption: str = None, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, parse_mode: str = None, duration: int = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future. [See Telegram API](https://core.telegram.org/bots/api#sendvoice)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `voice` :`(types.InputFile,str,)` Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `caption` :`str` Voice message caption, 0-1024 characters after entities parsing
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `parse_mode` :`str` Mode for parsing entities in the voice message caption. See formatting options for more details.
        - `duration` :`int` Duration of the voice message in seconds
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "voice": helper.toDict(voice, True),
            "caption": caption,
            "parse_mode": parse_mode,
            "duration": duration,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendVoice", data), types.Message)

    def sendVideoNote(self, chat_id: (int, str), video_note: (types.InputFile, str), reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, duration: int = None, length: int = None, thumb: (types.InputFile, str) = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """As of v.4.0, Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendvideonote)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `video_note` :`(types.InputFile,str,)` Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More info on Sending Files '. Sending video notes by a URL is currently unsupported
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `duration` :`int` Duration of sent video in seconds
        - `length` :`int` Video width and height, i.e. diameter of the video message
        - `thumb` :`(types.InputFile,str,)` Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://<file_attach_name>' if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files '
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "video_note": helper.toDict(video_note, True),
            "duration": duration,
            "length": length,
            "thumb": helper.toDict(thumb, True),
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendVideoNote", data), types.Message)

    def sendMediaGroup(self, chat_id: (int, str), media: list, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send a group of photos or videos as an album. On success, an array of the sent Messages is returned. [See Telegram API](https://core.telegram.org/bots/api#sendmediagroup)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `media` :`list` A JSON-serialized array describing photos and videos to be sent, must include 2-10 items
        - `disable_notification` :`bool` Sends the messages silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the messages are a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `list` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "media": media,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
        }
        return self.response(self.sendRequest("sendMediaGroup", data), list)

    def sendLocation(self, chat_id: (int, str), latitude: float, longitude: float, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, live_period: int = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send point on the map. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendlocation)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `latitude` :`float` Latitude of the location
        - `longitude` :`float` Longitude of the location
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `live_period` :`int` Period in seconds for which the location will be updated (see Live Locations, should be between 60 and 86400.
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "live_period": live_period,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendLocation", data), types.Message)

    def editMessageLiveLocation(self, latitude: float, longitude: float, chat_id: (int, str) = None, message_id: int = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None):
        """Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message was sent by the bot, the edited Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#editmessagelivelocation)

        - - - - -
        **Args**:

        - `latitude` :`float` Latitude of new location
        - `longitude` :`float` Longitude of new location
        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message to edit
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for a new inline keyboard.

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "latitude": latitude,
            "longitude": longitude,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("editMessageLiveLocation", data), None)

    def stopMessageLiveLocation(self, chat_id: (int, str) = None, message_id: int = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None):
        """Use this method to stop updating a live location message before live_period expires. On success, if the message was sent by the bot, the sent Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#stopmessagelivelocation)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message with live location to stop
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for a new inline keyboard.

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("stopMessageLiveLocation", data), None)

    def sendVenue(self, chat_id: (int, str), latitude: float, longitude: float, title: str, address: str, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, foursquare_id: str = None, foursquare_type: str = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send information about a venue. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendvenue)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `latitude` :`float` Latitude of the venue
        - `longitude` :`float` Longitude of the venue
        - `title` :`str` Name of the venue
        - `address` :`str` Address of the venue
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `foursquare_id` :`str` Foursquare identifier of the venue
        - `foursquare_type` :`str` Foursquare type of the venue, if known. (For example, 'arts_entertainment/default', 'arts_entertainment/aquarium' or 'food/icecream'.)
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
            "foursquare_id": foursquare_id,
            "foursquare_type": foursquare_type,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendVenue", data), types.Message)

    def sendContact(self, chat_id: (int, str), phone_number: str, first_name: str, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, last_name: str = None, vcard: str = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send phone contacts. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendcontact)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `phone_number` :`str` Contact's phone number
        - `first_name` :`str` Contact's first name
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove keyboard or to force a reply from the user.
        - `last_name` :`str` Contact's last name
        - `vcard` :`str` Additional data about the contact in the form of a vCard, 0-2048 bytes
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "vcard": vcard,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendContact", data), types.Message)

    def sendPoll(self, chat_id: (int, str), question: str, options: list, reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, is_anonymous: bool = None, type: str = None, allows_multiple_answers: bool = None, correct_option_id: int = None, explanation: str = None, explanation_parse_mode: str = None, open_period: int = None, close_date: int = None, is_closed: bool = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send a native poll. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendpoll)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `question` :`str` Poll question, 1-255 characters
        - `options` :`list` A JSON-serialized list of answer options, 2-10 strings 1-100 characters each
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `is_anonymous` :`bool` True, if the poll needs to be anonymous, defaults to True
        - `type` :`str` Poll type, 'quiz' or 'regular', defaults to 'regular'
        - `allows_multiple_answers` :`bool` True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False
        - `correct_option_id` :`int` 0-based identifier of the correct answer option, required for polls in quiz mode
        - `explanation` :`str` Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
        - `explanation_parse_mode` :`str` Mode for parsing entities in the explanation. See formatting options for more details.
        - `open_period` :`int` Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
        - `close_date` :`int` Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
        - `is_closed` :`bool` Pass True, if the poll needs to be immediately closed. This can be useful for poll preview.
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "question": question,
            "options": options,
            "is_anonymous": is_anonymous,
            "type": type,
            "allows_multiple_answers": allows_multiple_answers,
            "correct_option_id": correct_option_id,
            "explanation": explanation,
            "explanation_parse_mode": explanation_parse_mode,
            "open_period": open_period,
            "close_date": close_date,
            "is_closed": is_closed,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendPoll", data), types.Message)

    def sendDice(self, chat_id: (int, str), reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, emoji: str = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send a dice, which will have a random value from 1 to 6. On success, the sent Message is returned. (Yes, we're aware of the 'proper' singular of die. But it's awkward, and we decided to help it change. One dice at a time!) [See Telegram API](https://core.telegram.org/bots/api#senddice)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `emoji` :`str` Emoji on which the dice throw animation is based. Currently, must be one of '' or ''. Defauts to ''
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "emoji": emoji,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendDice", data), types.Message)

    def sendChatAction(self, chat_id: (int, str), action: str):
        """Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive. [See Telegram API](https://core.telegram.org/bots/api#sendchataction)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `action` :`str` Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_audio or upload_audio for audio files, upload_document for general files, find_location for location data, record_video_note or upload_video_note for video notes.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "action": action,
        }
        return self.response(self.sendRequest("sendChatAction", data), bool)

    def getUserProfilePhotos(self, user_id: int, offset: int = None, limit: int = None):
        """Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object. [See Telegram API](https://core.telegram.org/bots/api#getuserprofilephotos)

        - - - - -
        **Args**:

        - `user_id` :`int` Unique identifier of the target user
        - `offset` :`int` Sequential number of the first photo to be returned. By default, all photos are returned.
        - `limit` :`int` Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.

        **Returns:**

        - A `tuple`, on success a `types.UserProfilePhotos` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "offset": offset,
            "limit": limit,
        }
        return self.response(self.sendRequest("getUserProfilePhotos", data), types.UserProfilePhotos)

    def getFile(self, file_id: str):
        """Use this method to get basic info about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again. [See Telegram API](https://core.telegram.org/bots/api#getfile)

        - - - - -
        **Args**:

        - `file_id` :`str` File identifier to get info about

        **Returns:**

        - A `tuple`, on success a `types.File` as first member and a botApiResponse object as second member
        """
        data = {
            "file_id": file_id,
        }
        return self.response(self.sendRequest("getFile", data), types.File)

    def kickChatMember(self, chat_id: (int, str), user_id: int, until_date: int = None):
        """Use this method to kick a user from a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the group on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#kickchatmember)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        - `user_id` :`int` Unique identifier of the target user
        - `until_date` :`int` Date when the user will be unbanned, unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "until_date": until_date,
        }
        return self.response(self.sendRequest("kickChatMember", data), bool)

    def unbanChatMember(self, chat_id: (int, str), user_id: int):
        """Use this method to unban a previously kicked user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#unbanchatmember)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target group or username of the target supergroup or channel (in the format @username)
        - `user_id` :`int` Unique identifier of the target user

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        return self.response(self.sendRequest("unbanChatMember", data), bool)

    def restrictChatMember(self, chat_id: (int, str), user_id: int, permissions: types.ChatPermissions, until_date: int = None):
        """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate admin rights. Pass True for all permissions to lift restrictions from a user. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#restrictchatmember)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        - `user_id` :`int` Unique identifier of the target user
        - `permissions` :`types.ChatPermissions` New user permissions
        - `until_date` :`int` Date when restrictions will be lifted for the user, unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": helper.toDict(permissions, True),
            "until_date": until_date,
        }
        return self.response(self.sendRequest("restrictChatMember", data), bool)

    def promoteChatMember(self, chat_id: (int, str), user_id: int, can_change_info: bool = None, can_post_messages: bool = None, can_edit_messages: bool = None, can_delete_messages: bool = None, can_invite_users: bool = None, can_restrict_members: bool = None, can_pin_messages: bool = None, can_promote_members: bool = None):
        """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Pass False for all boolean parameters to demote a user. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#promotechatmember)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `user_id` :`int` Unique identifier of the target user
        - `can_change_info` :`bool` Pass True, if the administrator can change chat title, photo and other settings
        - `can_post_messages` :`bool` Pass True, if the administrator can create channel posts, channels only
        - `can_edit_messages` :`bool` Pass True, if the administrator can edit messages of other users and can pin messages, channels only
        - `can_delete_messages` :`bool` Pass True, if the administrator can delete messages of other users
        - `can_invite_users` :`bool` Pass True, if the administrator can invite new users to the chat
        - `can_restrict_members` :`bool` Pass True, if the administrator can restrict, ban or unban chat members
        - `can_pin_messages` :`bool` Pass True, if the administrator can pin messages, supergroups only
        - `can_promote_members` :`bool` Pass True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by him)

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "can_change_info": can_change_info,
            "can_post_messages": can_post_messages,
            "can_edit_messages": can_edit_messages,
            "can_delete_messages": can_delete_messages,
            "can_invite_users": can_invite_users,
            "can_restrict_members": can_restrict_members,
            "can_pin_messages": can_pin_messages,
            "can_promote_members": can_promote_members,
        }
        return self.response(self.sendRequest("promoteChatMember", data), bool)

    def setChatAdministratorCustomTitle(self, chat_id: (int, str), user_id: int, custom_title: str):
        """Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchatadministratorcustomtitle)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        - `user_id` :`int` Unique identifier of the target user
        - `custom_title` :`str` New custom title for the administrator; 0-16 characters, emoji are not allowed

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "custom_title": custom_title,
        }
        return self.response(self.sendRequest("setChatAdministratorCustomTitle", data), bool)

    def setChatPermissions(self, chat_id: (int, str), permissions: types.ChatPermissions):
        """Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchatpermissions)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        - `permissions` :`types.ChatPermissions` New default chat permissions

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "permissions": helper.toDict(permissions, True),
        }
        return self.response(self.sendRequest("setChatPermissions", data), bool)

    def exportChatInviteLink(self, chat_id: (int, str)):
        """Use this method to generate a new invite link for a chat; any previously generated link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns the new invite link as String on success. [See Telegram API](https://core.telegram.org/bots/api#exportchatinvitelink)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `str` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("exportChatInviteLink", data), str)

    def setChatPhoto(self, chat_id: (int, str), photo: types.InputFile):
        """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchatphoto)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `photo` :`types.InputFile` New chat photo, uploaded using multipart/form-data

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "photo": helper.toDict(photo, True),
        }
        return self.response(self.sendRequest("setChatPhoto", data), bool)

    def deleteChatPhoto(self, chat_id: (int, str)):
        """Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#deletechatphoto)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("deleteChatPhoto", data), bool)

    def setChatTitle(self, chat_id: (int, str), title: str):
        """Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchattitle)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `title` :`str` New chat title, 1-255 characters

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "title": title,
        }
        return self.response(self.sendRequest("setChatTitle", data), bool)

    def setChatDescription(self, chat_id: (int, str), description: str = None):
        """Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchatdescription)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `description` :`str` New chat description, 0-255 characters

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "description": description,
        }
        return self.response(self.sendRequest("setChatDescription", data), bool)

    def pinChatMessage(self, chat_id: (int, str), message_id: int, disable_notification: bool = None):
        """Use this method to pin a message in a group, a supergroup, or a channel. The bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' admin right in the supergroup or 'can_edit_messages' admin right in the channel. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#pinchatmessage)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Identifier of a message to pin
        - `disable_notification` :`bool` Pass True, if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "disable_notification": disable_notification,
        }
        return self.response(self.sendRequest("pinChatMessage", data), bool)

    def unpinChatMessage(self, chat_id: (int, str)):
        """Use this method to unpin a message in a group, a supergroup, or a channel. The bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' admin right in the supergroup or 'can_edit_messages' admin right in the channel. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#unpinchatmessage)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("unpinChatMessage", data), bool)

    def leaveChat(self, chat_id: (int, str)):
        """Use this method for your bot to leave a group, supergroup or channel. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#leavechat)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("leaveChat", data), bool)

    def getChat(self, chat_id: (int, str)):
        """Use this method to get up to date information about the chat (current name of the user for one-on-one conversations, current username of a user, group or channel, etc.). Returns a Chat object on success. [See Telegram API](https://core.telegram.org/bots/api#getchat)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `types.Chat` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("getChat", data), types.Chat)

    def getChatAdministrators(self, chat_id: (int, str)):
        """Use this method to get a list of administrators in a chat. On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots. If the chat is a group or a supergroup and no administrators were appointed, only the creator will be returned. [See Telegram API](https://core.telegram.org/bots/api#getchatadministrators)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `list` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("getChatAdministrators", data), list)

    def getChatMembersCount(self, chat_id: (int, str)):
        """Use this method to get the number of members in a chat. Returns Int on success. [See Telegram API](https://core.telegram.org/bots/api#getchatmemberscount)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)

        **Returns:**

        - A `tuple`, on success a `int` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("getChatMembersCount", data), int)

    def getChatMember(self, chat_id: (int, str), user_id: int):
        """Use this method to get information about a member of a chat. Returns a ChatMember object on success. [See Telegram API](https://core.telegram.org/bots/api#getchatmember)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        - `user_id` :`int` Unique identifier of the target user

        **Returns:**

        - A `tuple`, on success a `types.ChatMember` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        return self.response(self.sendRequest("getChatMember", data), types.ChatMember)

    def setChatStickerSet(self, chat_id: (int, str), sticker_set_name: str):
        """Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setchatstickerset)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        - `sticker_set_name` :`str` Name of the sticker set to be set as the group sticker set

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "sticker_set_name": sticker_set_name,
        }
        return self.response(self.sendRequest("setChatStickerSet", data), bool)

    def deleteChatStickerSet(self, chat_id: (int, str)):
        """Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#deletechatstickerset)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
        }
        return self.response(self.sendRequest("deleteChatStickerSet", data), bool)

    def answerCallbackQuery(self, callback_query_id: str, text: str = None, show_alert: bool = None, url: str = None, cache_time: int = None):
        """Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned. [See Telegram API](https://core.telegram.org/bots/api#answercallbackquery)

        - - - - -
        **Args**:

        - `callback_query_id` :`str` Unique identifier for the query to be answered
        - `text` :`str` Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
        - `show_alert` :`bool` If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
        - `url` :`str` URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your game ' note that this will only work if the query comes from a callback_game button.Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
        - `cache_time` :`int` The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time,
        }
        return self.response(self.sendRequest("answerCallbackQuery", data), bool)

    def setMyCommands(self, commands: list):
        """Use this method to change the list of the bot's commands. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setmycommands)

        - - - - -
        **Args**:

        - `commands` :`list` A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "commands": commands,
        }
        return self.response(self.sendRequest("setMyCommands", data), bool)

    def getMyCommands(self, ):
        """Use this method to get the current list of the bot's commands. Requires no parameters. Returns Array of BotCommand on success. [See Telegram API](https://core.telegram.org/bots/api#getmycommands)

        - - - - -
        **Args**:


        **Returns:**

        - A `tuple`, on success a `list` as first member and a botApiResponse object as second member
        """
        data = {
        }
        return self.response(self.sendRequest("getMyCommands", data), list)

    def editMessageText(self, text: str, chat_id: (int, str) = None, message_id: int = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None, parse_mode: str = None, disable_web_page_preview: bool = None):
        """Use this method to edit text and game messages. On success, if edited message is sent by the bot, the edited Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#editmessagetext)

        - - - - -
        **Args**:

        - `text` :`str` New text of the message, 1-4096 characters after entities parsing
        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message to edit
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for an inline keyboard.
        - `parse_mode` :`str` Mode for parsing entities in the message text. See formatting options for more details.
        - `disable_web_page_preview` :`bool` Disables link previews for links in this message

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        if disable_web_page_preview is None:
            disable_web_page_preview = self.default_disable_web_preview

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("editMessageText", data), None)

    def editMessageCaption(self, chat_id: (int, str) = None, message_id: int = None, caption: str = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None, parse_mode: str = None):
        """Use this method to edit captions of messages. On success, if edited message is sent by the bot, the edited Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#editmessagecaption)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message to edit
        - `caption` :`str` New caption of the message, 0-1024 characters after entities parsing
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for an inline keyboard.
        - `parse_mode` :`str` Mode for parsing entities in the message caption. See formatting options for more details.

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        if parse_mode is None:
            parse_mode = self.default_parse_mode

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("editMessageCaption", data), None)

    def editMessageMedia(self, media: types.InputMedia, chat_id: (int, str) = None, message_id: int = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None):
        """Use this method to edit animation, audio, document, photo, or video messages. If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded. Use previously uploaded file via its file_id or specify a URL. On success, if the edited message was sent by the bot, the edited Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#editmessagemedia)

        - - - - -
        **Args**:

        - `media` :`types.InputMedia` A JSON-serialized object for a new media content of the message
        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message to edit
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for a new inline keyboard.

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "media": helper.toDict(media, True),
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("editMessageMedia", data), None)

    def editMessageReplyMarkup(self, chat_id: (int, str) = None, message_id: int = None, inline_message_id: str = None, reply_markup: types.InlineKeyboardMarkup = None):
        """Use this method to edit only the reply markup of messages. On success, if edited message is sent by the bot, the edited Message is returned, otherwise True is returned. [See Telegram API](https://core.telegram.org/bots/api#editmessagereplymarkup)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the message to edit
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for an inline keyboard.

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("editMessageReplyMarkup", data), None)

    def stopPoll(self, chat_id: (int, str), message_id: int, reply_markup: types.InlineKeyboardMarkup = None):
        """Use this method to stop a poll which was sent by the bot. On success, the stopped Poll with the final results is returned. [See Telegram API](https://core.telegram.org/bots/api#stoppoll)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Identifier of the original message with the poll
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for a new message inline keyboard.

        **Returns:**

        - A `tuple`, on success a `types.Poll` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("stopPoll", data), types.Poll)

    def deleteMessage(self, chat_id: (int, str), message_id: int):
        """Use this method to delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours ago.- A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.- Bots can delete outgoing messages in private chats, groups, and supergroups.- Bots can delete incoming messages in private chats.- Bots granted can_post_messages permissions can delete outgoing messages in channels.- If the bot is an administrator of a group, it can delete any message there.- If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#deletemessage)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `message_id` :`int` Identifier of the message to delete

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        return self.response(self.sendRequest("deleteMessage", data), bool)

    def sendSticker(self, chat_id: (int, str), sticker: (types.InputFile, str), reply_markup: (types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply) = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send static .WEBP or animated .TGS stickers. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendsticker)

        - - - - -
        **Args**:

        - `chat_id` :`(int,str,)` Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        - `sticker` :`(types.InputFile,str,)` Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `reply_markup` :`(types.InlineKeyboardMarkup,types.ReplyKeyboardMarkup,types.ReplyKeyboardRemove,types.ForceReply,)` Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "sticker": helper.toDict(sticker, True),
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendSticker", data), types.Message)

    def getStickerSet(self, name: str):
        """Use this method to get a sticker set. On success, a StickerSet object is returned. [See Telegram API](https://core.telegram.org/bots/api#getstickerset)

        - - - - -
        **Args**:

        - `name` :`str` Name of the sticker set

        **Returns:**

        - A `tuple`, on success a `types.StickerSet` as first member and a botApiResponse object as second member
        """
        data = {
            "name": name,
        }
        return self.response(self.sendRequest("getStickerSet", data), types.StickerSet)

    def uploadStickerFile(self, user_id: int, png_sticker: types.InputFile):
        """Use this method to upload a .PNG file with a sticker for later use in createNewStickerSet and addStickerToSet methods (can be used multiple times). Returns the uploaded File on success. [See Telegram API](https://core.telegram.org/bots/api#uploadstickerfile)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier of sticker file owner
        - `png_sticker` :`types.InputFile` PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. More info on Sending Files '

        **Returns:**

        - A `tuple`, on success a `types.File` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "png_sticker": helper.toDict(png_sticker, True),
        }
        return self.response(self.sendRequest("uploadStickerFile", data), types.File)

    def createNewStickerSet(self, user_id: int, name: str, title: str, emojis: str, png_sticker: (types.InputFile, str) = None, tgs_sticker: types.InputFile = None, contains_masks: bool = None, mask_position: types.MaskPosition = None):
        """Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. You must use exactly one of the fields png_sticker or tgs_sticker. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#createnewstickerset)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier of created sticker set owner
        - `name` :`str` Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only english letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in '_by_<bot username>'. <bot_username> is case insensitive. 1-64 characters.
        - `title` :`str` Sticker set title, 1-64 characters
        - `emojis` :`str` One or more emoji corresponding to the sticker
        - `png_sticker` :`(types.InputFile,str,)` PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `tgs_sticker` :`types.InputFile` TGS animation with the sticker, uploaded using multipart/form-data. See https://core.telegram.org/animated_stickers#technical-requirements for technical requirements
        - `contains_masks` :`bool` Pass True, if a set of mask stickers should be created
        - `mask_position` :`types.MaskPosition` A JSON-serialized object for position where the mask should be placed on faces

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "name": name,
            "title": title,
            "png_sticker": helper.toDict(png_sticker, True),
            "tgs_sticker": helper.toDict(tgs_sticker, True),
            "emojis": emojis,
            "contains_masks": contains_masks,
            "mask_position": helper.toDict(mask_position, True),
        }
        return self.response(self.sendRequest("createNewStickerSet", data), bool)

    def addStickerToSet(self, user_id: int, name: str, png_sticker: (types.InputFile, str), emojis: str, tgs_sticker: types.InputFile = None, mask_position: types.MaskPosition = None):
        """Use this method to add a new sticker to a set created by the bot. You must use exactly one of the fields png_sticker or tgs_sticker. Animated stickers can be added to animated sticker sets and only to them. Animated sticker sets can have up to 50 stickers. Static sticker sets can have up to 120 stickers. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#addstickertoset)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier of sticker set owner
        - `name` :`str` Sticker set name
        - `png_sticker` :`(types.InputFile,str,)` PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '
        - `emojis` :`str` One or more emoji corresponding to the sticker
        - `tgs_sticker` :`types.InputFile` TGS animation with the sticker, uploaded using multipart/form-data. See https://core.telegram.org/animated_stickers#technical-requirements for technical requirements
        - `mask_position` :`types.MaskPosition` A JSON-serialized object for position where the mask should be placed on faces

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "name": name,
            "png_sticker": helper.toDict(png_sticker, True),
            "tgs_sticker": helper.toDict(tgs_sticker, True),
            "emojis": emojis,
            "mask_position": helper.toDict(mask_position, True),
        }
        return self.response(self.sendRequest("addStickerToSet", data), bool)

    def setStickerPositionInSet(self, sticker: str, position: int):
        """Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setstickerpositioninset)

        - - - - -
        **Args**:

        - `sticker` :`str` File identifier of the sticker
        - `position` :`int` New sticker position in the set, zero-based

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "sticker": sticker,
            "position": position,
        }
        return self.response(self.sendRequest("setStickerPositionInSet", data), bool)

    def deleteStickerFromSet(self, sticker: str):
        """Use this method to delete a sticker from a set created by the bot. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#deletestickerfromset)

        - - - - -
        **Args**:

        - `sticker` :`str` File identifier of the sticker

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "sticker": sticker,
        }
        return self.response(self.sendRequest("deleteStickerFromSet", data), bool)

    def setStickerSetThumb(self, user_id: int, name: str, thumb: (types.InputFile, str) = None):
        """Use this method to set the thumbnail of a sticker set. Animated thumbnails can be set for animated sticker sets only. Returns True on success. [See Telegram API](https://core.telegram.org/bots/api#setstickersetthumb)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier of the sticker set owner
        - `name` :`str` Sticker set name
        - `thumb` :`(types.InputFile,str,)` A PNG image with the thumbnail, must be up to 128 kilobytes in size and have width and height exactly 100px, or a TGS animation with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/animated_stickers#technical-requirements for animated sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files '. Animated sticker set thumbnail can't be uploaded via HTTP URL.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "name": name,
            "user_id": user_id,
            "thumb": helper.toDict(thumb, True),
        }
        return self.response(self.sendRequest("setStickerSetThumb", data), bool)

    def answerInlineQuery(self, inline_query_id: str, results: list, cache_time: int = None, is_personal: bool = None, next_offset: str = None, switch_pm_text: str = None, switch_pm_parameter: str = None):
        """Use this method to send answers to an inline query. On success, True is returned.No more than 50 results per query are allowed. [See Telegram API](https://core.telegram.org/bots/api#answerinlinequery)

        - - - - -
        **Args**:

        - `inline_query_id` :`str` Unique identifier for the answered query
        - `results` :`list` A JSON-serialized array of results for the inline query
        - `cache_time` :`int` The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
        - `is_personal` :`bool` Pass True, if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query
        - `next_offset` :`str` Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
        - `switch_pm_text` :`str` If passed, clients will display a button with specified text that switches the user to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter
        - `switch_pm_parameter` :`str` Deep-linking parameter for the /start message sent to the bot when user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube account to adapt search results accordingly. To do this, it displays a 'Connect your YouTube account' button above the results, or even before showing any. The user presses the button, switches to a private chat with the bot and, in doing so, passes a start parameter that instructs the bot to return an oauth link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat where they wanted to use the bot's inline capabilities.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "inline_query_id": inline_query_id,
            "results": results,
            "cache_time": cache_time,
            "is_personal": is_personal,
            "next_offset": next_offset,
            "switch_pm_text": switch_pm_text,
            "switch_pm_parameter": switch_pm_parameter,
        }
        return self.response(self.sendRequest("answerInlineQuery", data), bool)

    def sendInvoice(self, chat_id: int, title: str, description: str, payload: str, provider_token: str, start_parameter: str, currency: str, prices: list, reply_markup: types.InlineKeyboardMarkup = None, provider_data: str = None, photo_url: str = None, photo_size: int = None, photo_width: int = None, photo_height: int = None, need_name: bool = None, need_phone_number: bool = None, need_email: bool = None, need_shipping_address: bool = None, send_phone_number_to_provider: bool = None, send_email_to_provider: bool = None, is_flexible: bool = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send invoices. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendinvoice)

        - - - - -
        **Args**:

        - `chat_id` :`int` Unique identifier for the target private chat
        - `title` :`str` Product name, 1-32 characters
        - `description` :`str` Product description, 1-255 characters
        - `payload` :`str` Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.
        - `provider_token` :`str` Payments provider token, obtained via Botfather
        - `start_parameter` :`str` Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter
        - `currency` :`str` Three-letter ISO 4217 currency code, see more on currencies
        - `prices` :`list` Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
        - `provider_data` :`str` JSON-encoded data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
        - `photo_url` :`str` URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
        - `photo_size` :`int` Photo size
        - `photo_width` :`int` Photo width
        - `photo_height` :`int` Photo height
        - `need_name` :`bool` Pass True, if you require the user's full name to complete the order
        - `need_phone_number` :`bool` Pass True, if you require the user's phone number to complete the order
        - `need_email` :`bool` Pass True, if you require the user's email address to complete the order
        - `need_shipping_address` :`bool` Pass True, if you require the user's shipping address to complete the order
        - `send_phone_number_to_provider` :`bool` Pass True, if user's phone number should be sent to provider
        - `send_email_to_provider` :`bool` Pass True, if user's email address should be sent to provider
        - `is_flexible` :`bool` Pass True, if the final price depends on the shipping method
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "start_parameter": start_parameter,
            "currency": currency,
            "prices": prices,
            "provider_data": provider_data,
            "photo_url": photo_url,
            "photo_size": photo_size,
            "photo_width": photo_width,
            "photo_height": photo_height,
            "need_name": need_name,
            "need_phone_number": need_phone_number,
            "need_email": need_email,
            "need_shipping_address": need_shipping_address,
            "send_phone_number_to_provider": send_phone_number_to_provider,
            "send_email_to_provider": send_email_to_provider,
            "is_flexible": is_flexible,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendInvoice", data), types.Message)

    def answerShippingQuery(self, shipping_query_id: str, ok: bool, shipping_options: list = None, error_message: str = None):
        """If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned. [See Telegram API](https://core.telegram.org/bots/api#answershippingquery)

        - - - - -
        **Args**:

        - `shipping_query_id` :`str` Unique identifier for the query to be answered
        - `ok` :`bool` Specify True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
        - `shipping_options` :`list` Required if ok is True. A JSON-serialized array of available shipping options.
        - `error_message` :`str` Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable'). Telegram will display this message to the user.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "shipping_query_id": shipping_query_id,
            "ok": ok,
            "shipping_options": shipping_options,
            "error_message": error_message,
        }
        return self.response(self.sendRequest("answerShippingQuery", data), bool)

    def answerPreCheckoutQuery(self, pre_checkout_query_id: str, ok: bool, error_message: str = None):
        """Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent. [See Telegram API](https://core.telegram.org/bots/api#answerprecheckoutquery)

        - - - - -
        **Args**:

        - `pre_checkout_query_id` :`str` Unique identifier for the query to be answered
        - `ok` :`bool` Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
        - `error_message` :`str` Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "pre_checkout_query_id": pre_checkout_query_id,
            "ok": ok,
            "error_message": error_message,
        }
        return self.response(self.sendRequest("answerPreCheckoutQuery", data), bool)

    def setPassportDataErrors(self, user_id: int, errors: list):
        """Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns True on success.
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason. For example, if a birthday date seems invalid, a submitted document is blurry, a scan shows evidence of tampering, etc. Supply some details in the error message to make sure the user knows how to correct the issues. [See Telegram API](https://core.telegram.org/bots/api#setpassportdataerrors)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier
        - `errors` :`list` A JSON-serialized array describing the errors

        **Returns:**

        - A `tuple`, on success a `bool` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "errors": errors,
        }
        return self.response(self.sendRequest("setPassportDataErrors", data), bool)

    def sendGame(self, chat_id: int, game_short_name: str, reply_markup: types.InlineKeyboardMarkup = None, disable_notification: bool = None, reply_to_message_id: int = None):
        """Use this method to send a game. On success, the sent Message is returned. [See Telegram API](https://core.telegram.org/bots/api#sendgame)

        - - - - -
        **Args**:

        - `chat_id` :`int` Unique identifier for the target chat
        - `game_short_name` :`str` Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.
        - `reply_markup` :`types.InlineKeyboardMarkup` A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        - `disable_notification` :`bool` Sends the message silently. Users will receive a notification with no sound.
        - `reply_to_message_id` :`int` If the message is a reply, ID of the original message

        **Returns:**

        - A `tuple`, on success a `types.Message` as first member and a botApiResponse object as second member
        """
        if disable_notification is None:
            disable_notification = self.default_disable_notifications

        data = {
            "chat_id": chat_id,
            "game_short_name": game_short_name,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": helper.toDict(reply_markup, True),
        }
        return self.response(self.sendRequest("sendGame", data), types.Message)

    def setGameScore(self, user_id: int, score: int, chat_id: int = None, message_id: int = None, inline_message_id: str = None, force: bool = None, disable_edit_message: bool = None):
        """Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True. Returns an error, if the new score is not greater than the user's current score in the chat and force is False. [See Telegram API](https://core.telegram.org/bots/api#setgamescore)

        - - - - -
        **Args**:

        - `user_id` :`int` User identifier
        - `score` :`int` New score, must be non-negative
        - `chat_id` :`int` Required if inline_message_id is not specified. Unique identifier for the target chat
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the sent message
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message
        - `force` :`bool` Pass True, if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters
        - `disable_edit_message` :`bool` Pass True, if the game message should not be automatically edited to include the current scoreboard

        **Returns:**

        - A `tuple`, on success a `None` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "score": score,
            "force": force,
            "disable_edit_message": disable_edit_message,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
        }
        return self.response(self.sendRequest("setGameScore", data), None)

    def getGameHighScores(self, user_id: int, chat_id: int = None, message_id: int = None, inline_message_id: str = None):
        """Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. On success, returns an Array of GameHighScore objects. [See Telegram API](https://core.telegram.org/bots/api#getgamehighscores)

        - - - - -
        **Args**:

        - `user_id` :`int` Target user id
        - `chat_id` :`int` Required if inline_message_id is not specified. Unique identifier for the target chat
        - `message_id` :`int` Required if inline_message_id is not specified. Identifier of the sent message
        - `inline_message_id` :`str` Required if chat_id and message_id are not specified. Identifier of the inline message

        **Returns:**

        - A `tuple`, on success a `list` as first member and a botApiResponse object as second member
        """
        data = {
            "user_id": user_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
        }
        return self.response(self.sendRequest("getGameHighScores", data), list)

