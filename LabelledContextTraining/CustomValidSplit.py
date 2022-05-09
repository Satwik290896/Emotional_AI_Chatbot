import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Input, Dropout, LSTM, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.initializers import glorot_uniform
from emo_utils_second import *
import matplotlib.pyplot as plt

np.random.seed(1)

def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()`

    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this.

    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """

    m = X.shape[0]  # number of training examples
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    X_indices = np.zeros((m, max_len))

    for i in range(m):  # loop over training examples
        # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
        sentence_words = (X[i].lower()).split()
        # Initialize j to 0
        j = 0
        # Loop over the words of sentence_words
        #print(sentence_words)
        for w in sentence_words:
            # Set the (i,j)th entry of X_indices to the index of the correct word.
            X_indices[i, j] = word_to_index[w]
            # Increment j to j + 1
            j = j + 1
    return X_indices

def pretrained_embedding_layer(word_to_vec_map, word_to_index):
    """
    Creates a Keras Embedding() layer and loads in pre-trained GloVe 50-dimensional vectors.

    Arguments:
    word_to_vec_map -- dictionary mapping words to their GloVe vector representation.
    word_to_index -- dictionary mapping from words to their indices in the vocabulary (400,001 words)

    Returns:
    embedding_layer -- pretrained layer Keras instance
    """
    vocab_len = len(word_to_index) + 1  # adding 1 to fit Keras embedding (requirement)
    emb_dim = word_to_vec_map["cucumber"].shape[0]  # define dimensionality of your GloVe word vectors (= 50)

    # Initialize the embedding matrix as a numpy array of zeros of shape (vocab_len, dimensions of word vectors = emb_dim)
    emb_matrix = np.zeros((vocab_len, emb_dim))

    # Set each row "index" of the embedding matrix to be the word vector representation of the "index"th word of the vocabulary
    for word, index in word_to_index.items():
        emb_matrix[index, :] = word_to_vec_map[word]

    # Define Keras embedding layer with the correct output/input sizes, make it trainable. Use Embedding(...). Make sure to set trainable=False.
    embedding_layer = Embedding(vocab_len, emb_dim)

    # Build the embedding layer, it is required before setting the weights of the embedding layer. Do not modify the "None".
    embedding_layer.build((None,))

    # Set the weights of the embedding layer to the embedding matrix. Your layer is now pretrained.
    embedding_layer.set_weights([emb_matrix])

    return embedding_layer


def SentimentAnalysis(input_shape, word_to_vec_map, word_to_index):
    """
    Function creating the Emojify-v2 model's graph.

    Arguments:
    input_shape -- shape of the input, usually (max_len,)
    word_to_vec_map -- dictionary mapping every word in a vocabulary into its 50-dimensional vector representation
    word_to_index -- dictionary mapping from words to their indices in the vocabulary (400,001 words)

    Returns:
    model -- a model instance in Keras
    """
    # Define sentence_indices as the input of the graph, it should be of shape input_shape and dtype 'int32' (as it contains indices).
    sentence_indices = Input(shape=input_shape, dtype=np.int32)

    # Create the embedding layer pretrained with GloVe Vectors (≈1 line)
    embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)

    # Propagate sentence_indices through your embedding layer, you get back the embeddings
    embeddings = embedding_layer(sentence_indices)

    # Propagate the embeddings through an LSTM layer with 128-dimensional hidden state
    # Be careful, the returned output should be a batch of sequences.
    X = LSTM(128, return_sequences=True)(embeddings)
    # Add dropout with a probability of 0.5
    X = Dropout(0.5)(X)
    # Propagate X trough another LSTM layer with 128-dimensional hidden state
    # Be careful, the returned output should be a single hidden state, not a batch of sequences.
    X = LSTM(128)(X)
    # Add dropout with a probability of 0.5
    X = Dropout(0.5)(X)
    # Propagate X through a Dense layer with softmax activation to get back a batch of 5-dimensional vectors.
    X = Dense(10, activation='softmax')(X)
    # Add a softmax activation
    X = Activation('softmax')(X)

    # Create Model instance which converts sentence_indices into X.
    model = Model(sentence_indices, X)

    return model

def custom_loss(y_true,y_pred):
   # if y_true<5 and y_pred>=5:
    cce = tf.keras.losses.CategoricalCrossentropy()
    '''if tf.math.argmax(y_true)[0]<5:
        if tf.math.argmax(y_pred)[0]>=5:
            loss = cce(y_true, y_pred)
        else:
            loss = 2*(cce(y_true,y_pred))
    else:
        if tf.math.argmax(y_pred)[0]<5:
            loss = cce(y_true,y_pred)
        else:
            loss = 2*(cce(y_true,y_pred))'''

    if abs(tf.math.argmax(y_true)[0]-tf.math.argmax(y_pred)[0])==5:
        loss = cce(y_true,y_pred)/2
    else:
        loss = cce(y_true,y_pred)


    return loss

if __name__ == "__main__":
    f = open("Accuracy_every_100_epochs.txt","a+")
    f.write("\n\n\nI am starting now\n\n")
    # Read train and test files
    X_train, Y_train = read_csv('TrainDTS.csv')
    X_test, Y_test = read_csv('TestDTS.csv')
    maxLen = len(max(X_train, key=len).split())

    # Convert one-hot-encoding type, classification =5, [1,0,0,0,0]
    Y_oh_train = convert_to_one_hot(Y_train, C=10)
    Y_oh_test = convert_to_one_hot(Y_test, C=10)

    # Read 50 feature dimension glove file
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('glove.6B.50d.txt')

    # Model and model summmary
    model = SentimentAnalysis((maxLen,), word_to_vec_map, word_to_index)
    model.summary()
    model.compile(loss=custom_loss, optimizer='adam', metrics=['accuracy'])

    X_train_indices = sentences_to_indices(X_train, word_to_index, maxLen)
    Y_train_oh = convert_to_one_hot(Y_train, C=10)
    for k in range(1):
        # Train model
        NEpochs = 150*2
        BatchSiz = 4
        y_test_oh = convert_to_one_hot(Y_test,C=10)
        X_test_indices = sentences_to_indices(X_test,word_to_index,maxLen)
        history = model.fit(X_train_indices, Y_train_oh, epochs=NEpochs, batch_size=BatchSiz, shuffle=True,validation_split=0.3)

        X_test_indices = sentences_to_indices(X_test, word_to_index, max_len=maxLen)
        Y_test_oh = convert_to_one_hot(Y_test, C=10)

        # Evaluate model, loss and accuracy
        loss, acc = model.evaluate(X_test_indices, Y_test_oh)
        acc100 = acc*100
        f.write("%f\n" %acc100)
        print("Test accuracy = ", acc)

        # Compare prediction and expected emoji
        C = 10
        y_test_oh = np.eye(C)[Y_test.reshape(-1)]
        X_test_indices = sentences_to_indices(X_test, word_to_index, maxLen)
        pred = model.predict(X_test_indices)
        for i in range(len(X_test)):
            x = X_test_indices
            num = np.argmax(pred[i])
            #if (num != Y_test[i]):
            #print('Expected emoji:' + label_to_emoji(Y_test[i]) + ' prediction: ' + X_test[i] + label_to_emoji(num).strip())

        # Test your sentence
        x_test = np.array(['very happy'])
        X_test_indices = sentences_to_indices(x_test, word_to_index, maxLen)
        print(x_test[0] + ' ' + label_to_emoji(np.argmax(model.predict(X_test_indices))))


    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(range(1,len(history.history['accuracy'])+1),history.history['accuracy'])
    axs[0, 0].set_title('Train dataset Accuracy for BatchSize:%d' %BatchSiz)
    axs[1, 0].plot(range(1,len(history.history['loss'])+1),history.history['loss'],'tab:red')
    axs[1, 0].set_title('Training Loss for BatchSize:%d' %BatchSiz)
    axs[0, 1].plot(range(1,len(history.history['val_accuracy'])+1),history.history['val_accuracy'])
    axs[0, 1].set_title('Validation dataset Accuracy for BatchSize:%d' %BatchSiz)
    axs[1, 1].plot(range(1,len(history.history['val_loss'])+1),history.history['val_loss'],'tab:red')
    axs[1, 1].set_title('Validation Loss for BatchSize:%d' %BatchSiz)
    
    '''axs[0, 0].plot(history.history['accuracy'])
    axs[0, 0].set_title('Train dataset Accuracy')
    axs[0, 1].plot(history.history['loss'])
    axs[0, 1].set_title('Training Loss')
    axs[1, 0].plot(history.history['val_accuracy'])
    axs[1, 0].set_title('Validation dataset Accuracy')
    axs[1, 1].plot(history.history['val_loss'])
    axs[1, 1].set_title('Validation Loss')'''
    for ax in axs.flat:
        ax.set(xlabel='Epochs', ylabel='Parameter')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    '''for ax in axs.flat:
        ax.label_outer()'''

    plt.show()
