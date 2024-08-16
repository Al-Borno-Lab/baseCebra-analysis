from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
import sklearn.metrics
from cebra import CEBRA
import numpy as np
import pandas as pd

def trainAllKin(emb_train, label_train, n_neighbors=128):

    decoder_list = [KNeighborsRegressor(n_neighbors, metric = 'cosine') for _ in range(label_train.shape[1])]

    # train
    for i, decoder in enumerate(decoder_list):
        decoder.fit(emb_train, label_train[:,i])

    return decoder_list


class model:
    def __init__(self) -> None:
        pass

    def train(self, neural_session, continous_sessions):
        max_iterations = 2000 #default is 5000.
        output_dimension = 64 #here, we set as a variable for hypothesis testing below.

        # intiate the model
        self.cebra_posOnly_model = CEBRA(
                        model_architecture='offset10-model',
                        batch_size=512,
                        learning_rate=5e-5, # 1e-6
                        temperature= 0.1, # 0.2
                        output_dimension=output_dimension,
                        max_iterations=max_iterations,
                        distance='cosine',
                        conditional='time_delta',
                        device='cuda_if_available',
                        verbose=True,
                        time_offsets=10)

        nStack_train = np.vstack(neural_session)
        cStack_train = np.vstack(continous_sessions)


        # train conditioned on position data only
        self.cebra_posOnly_model.fit(nStack_train, cStack_train)

        # fit decoder
        emb = self.cebra_posOnly_model.transform(nStack_train)
        fullKin = trainAllKin(emb, cStack_train)

        self.decoder = fullKin

    def predict(self, neural_session):

        out = []

        for n in neural_session:
            emb_ = self.cebra_posOnly_model.transform(n)

            out_kin = []
            for i, decoder in enumerate(self.decoder):
                out_kin += [decoder.predict(emb_)]

            out += [np.asarray(out_kin)]

        return out

    def get_embedding(self, neural_session):

        out = []
        for n in neural_session:
          emb = self.cebra_posOnly_model.transform(n)
          out += [emb]
        return out

    def examine(self, neural_session, continous_sessions):

        # nStack_train = np.vstack(neural_session)
        # cStack_train = np.vstack(continous_sessions)
        r2 = []
        for n, c in zip(neural_session, continous_sessions):

          emb_test = self.cebra_posOnly_model.transform(n)

          test_score = []
          for i, decoder in enumerate(self.decoder):
              prediction = decoder.predict(emb_test)
              test_score += [
                  sklearn.metrics.r2_score(c[:, i], prediction)
              ]
          r2 += [test_score]

        return r2