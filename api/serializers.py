from rest_framework import serializers
from main.model.refbook import Refbook
from main.model.element import Element


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = ('id', 'code', 'name',)


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('code', 'value',)
