from models.BaseModel import BaseModel
from keras.models import Sequential
from keras.layers import *

class LSTM_CNN_model(BaseModel):
    """This is the LSTM-CNN model. It inherits from the `BaseModel` class.
    
    This class only implements the `build_model` function used to define and compile the keras model.

    Attributes
    ----------
    model_name : str
        The `model_name` parameter is used as a name for a checkpoint dictionary inside models checkpoints
        dictionary, for more details see `BaseModel` class.

    """
    def __init__(self, model_name):
        super().__init__(model_name)


    def build_model(self, embedding_matrix, seq_len, params):
        """This method is used to define and compile the keras model.
        
        The first layer always is the Embedding layer used to embed the word sequences to vector sequences 
        which then are send to the LSTM layer. The LSTM layer uses the global context to generate new representations 
        of the words. These new representations are send to the Convolutional layer which extract local features 
        from the data. After the Convolutional layer, there is MaxPooling layer which reduces the dimensionality 
        of the problem. In the end, there is a Dense layer which outputs the probability for the tweet being of 
        the first class.

        Parameters
        ----------
        embedding_matrix : ndarray
            Numpay matrix containing the GloVe embeddings for our training vocabulary.
        seq_len : ndarray
            The length of the tweet, in our case the number of word vectors every tweet should contain.
        params : dic
            Dictionary containing all the parameters for the model
        """
        self.model = Sequential()

        self.model.add(Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1], input_length=seq_len, \
                                 weights=[embedding_matrix], name='emb'))

        self.model.add(LSTM(units=params["LSTM_num_neurons"], dropout=params["LSTM_dropout"], recurrent_dropout=params["LSTM_recurrent_dropout"], return_sequences=True))

        self.model.add(Conv1D(filters=params["CNN_filters"], kernel_size=params["CNN_kernel_size"], activation=params["CNN_activation"]))
        
        self.model.add(MaxPooling1D(pool_size=params["CNN_pool_size"]))

        self.model.add(Flatten())
        self.model.add(Dense(1, activation=params["DENSE_activation"]))
        self.model.compile(loss=params["loss"], optimizer=params["optimizer"], metrics=['accuracy'])
