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
            if person.embedding is not None:
                self.push(person.embedding, person.id)
        print(f" ==== {len(self.dataset)} elements added from database ====")

    def push(self, emb, index):

        if type(emb) is str:
            db_emb = asarray(list(map(lambda x: float(x), emb.split(" "))))
        else:
            db_emb = emb
        if (index not in self.dataset) or (index in self.dataset and self.dataset[index] == ""):
            self.dataset[index] = db_emb
        else:
            print(" ==== index is already added ! ====")

    def delete(self, index):
        if index in self.dataset:
            self.dataset.pop(index)
        else:
            print("index is not in dataset !")

    def search(self, emb, dumyNum):
        result = {'hits': {'hits': []}}
        if len(self.dataset) == 0:
            print(" ===== no items in the dataset ==== ")
            return result

        for index, element_Emb in self.dataset.items():
            element_similarity = self.get_similarity(element_Emb, emb)
            result['hits']['hits'].append({"_score": element_similarity, "_id": index})

        return result

    def patch(self, emb, index):
        pass

    def get_similarity(self, emb1, emb2):
        print(f"elements in dataset  : {len(self.dataset)} ==========>")
        return (dot(emb1, emb2) / (norm(emb1)*norm(emb2))) + 1
