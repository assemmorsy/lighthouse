import json

from .singleton import Singleton
from ..models import KnownMissingPerson
from .classifier import Model

from numpy import dot, asarray
from numpy.linalg import norm


class SearchIndex(metaclass=Singleton):
    def __init__(self):
        self.dataset = {}
        people = KnownMissingPerson.objects.all()
        for person in people:
            self.push(person.embedding,person.id)

    def push(self, emb, index):
        if index not in self.dataset:
            self.dataset[index] = emb
        else:
            print("index is already added !")

    def delete(self, index):
        if index in self.dataset:
            self.dataset.pop(index)
        else:
            print("index is not in dataset !")

    def search(self, emb, dumyNum):
        result = {'hits': {'hits': []}}
        for index, element_Emb in self.dataset.items():
            db_emb = asarray(list(map(lambda x: float(x), element_Emb.split(" "))))

            element_similarity = self.get_similarity(db_emb, emb)
            result['hits']['hits'].append({"_score": element_similarity, "_id": index})

        return result

    def patch(self, emb, index):
        pass

    def get_similarity(self, emb1, emb2):
        return dot(emb1, emb2) / (norm(emb1)*norm(emb2))
