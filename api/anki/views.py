from typing import Any

from django.http import Http404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from anki.models import Deck, Card, DeckDescription, Stat
from anki.serializers import (DeckInfoSerializer,
                              DeckSerializer,
                              CardSerializer,
                              StatSerializer)

from api.settings import JWT_AUTH


class GetDecks(APIView):
    """
    Get all user's decks which are accessable to the requesting one.

    Endpoint: `api/get-decks?username={username}`

    Params: username, ?jwt 
    Logic: 
        1. Does the {username} user exist ? continue : 404 
        2. username <-> jwt ? send all decks : send public decks
    """
    def get(self, request: Request, format: Any = None) -> Response:
        username = request.query_params.get('username')
        # 1:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404   # no user with such username
        # 2:
        jwt_username = request.user.username
        if not JWT_AUTH or username == jwt_username:
        decks = Deck.objects.all().filter(owner=user)
        else:
            decks = (Deck.objects.all().filter(owner=user)
                                       .filter(public=True))
        serializer = DeckSerializer(decks, many=True)
        return Response(serializer.data)


class GetDeckInfo(APIView):
    """
    Get deck info if allowed.

    Endpoint: `api/get-deck-info?username={username}&deckname={deckname}`

    Params: username, deckname, ?jwt
    Logic:
        1. Does the {username} user exist ? continue : 404(user) 
        2. Does the {deckname} deck exist ? continue : 404(deck) 
        3. Is the deck public ? send deck info : continue
        4. username <-> jwt ? send deck info : 404(deck)
    """
    def get(self, request: Request, format: Any = None) -> Response:
        username = request.query_params.get('username')
        deckname = request.query_params.get('deckname')
        # 1:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404   # TODO: indicate that there's no user with
                            # the requested username
        # 2:
        try:
            deck: Deck = Deck.objects.get(owner=user, name=deckname)
        except Deck.DoesNotExist:
            raise Http404   # TODO: indicate that there's no deck with
                            # the requested name
        # 3&4:
        if JWT_AUTH and not deck.public:
            jwt_username = request.user.username
            if username != jwt_username:
                raise Http404   # TODO: indicate that there's no deck
                                # with the requested name
        serializer = DeckInfoSerializer(deck)
        return Response(serializer.data)


class GetDeckStats(APIView):
    """
    Get user's stats on a deck.

    Endpoint: `get-deck-stats?username={username}&deckname={deckname}`

    Get a username and deckname, return stats of a deck
    of a passed name of a user whose username is the passed one.
    If no such deck and/or user, return 404.

    TODO: auth and public/private decks
    """
    def get(self, request: Request, format: Any = None) -> Response:
        username = request.query_params.get('username')
        deckname = request.query_params.get('deckname')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404   # TODO: add meta info maybe

        try:
            deck = Deck.objects.get(owner=user, name=deckname)
        except Deck.DoesNotExist:
            raise Http404   # TODO: add meta info maybe

        # TODO: decide upon what to return as the stats
        return Response()


class GetDeckStuff(APIView):
    """
    Get all the stuff of a deck (i.e., name, color, public/private status,
    description, and cards) for update purposes.

    Endpoint: `get-deck-stuff?username={username}&deckname={deckname}`

    TODO: auth
    """
    def get(self, request: Request, format: Any = None) -> Response:
        username = request.query_params.get('username')
        deckname = request.query_params.get('deckname')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404   # TODO: add meta info maybe

        try:
            deck = Deck.objects.get(owner=user, name=deckname)
        except Deck.DoesNotExist:
            raise Http404   # TODO: add meta info maybe

        cards = Card.objects.filter(deck=deck)

        deck_serializer = DeckInfoSerializer(deck)
        card_serializer = CardSerializer(cards, many=True)
        return Response({
                'deck': deck_serializer.data,
                'cards': card_serializer.data
            })


class UpdateDeckStuff(APIView):
    """
    Update a deck's stuff (i.e., name, color, public/private status,
    description, and cards).

    Endpoint: `api/update-deck-stuff`

    TODO: auth
    """
    def post(self, request: Request, format: Any = None) -> Response:
        username = request.query_params.get('username')
        deckinfo = request.data.get('deck')
        cards = request.data.get('cards')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404   # TODO: add meta info maybe

        try:
            deck = Deck.objects.get(owner=user, pk=deckinfo.id)
            deck.name = deckinfo.name
            deck.color = deckinfo.color
            deck.public = deckinfo.public
        except Deck.DoesNotExist:
            deck = Deck(name=deckinfo.name, color=deckinfo.color,
                        public=deckinfo.public, owner=user)
        deck.save()
            
        try:
            description = DeckDescription.objects.get(deck=deck)
            description.description = deckinfo.description
        except DeckDescription.DoesNotExist:
            description = DeckDescription(description=deckinfo.description,
                                          deck=deck)
        description.save()

        for card in cards:
            try:
                card_in_db = Card.objects.get(pk=card.id)
                card_in_db.question = card.question
                card_in_db.answer = card.answer
            except Card.DoesNotExist:
                card_in_db = Card(question = card.question,
                                  answer = card.answer,
                                  deck=deck)
            card_in_db.save()

        return Response()


class PullNextCard(APIView):
    """
    Get a not-exactly-random card from a deck.
    To clarify: "not-exactly-random" means the next card that
    the backend find appropriate to give to a user.
    """
    def get(self, request: Request, format: Any = None) -> Response:
        pass  # here the app supposedly accesses all the stats on
              # a deck and decides what card is the most suitable to
              # return.


class PostFeedback(APIView):
    """
    Post feedback on a card that a user got.
    """
    def post(self, request: Request, format: Any = None) -> Response:
        pass
