#### Libraries
# Standard library
import json
import random
import sys
import mentor
import math

# Third-party libraries
import numpy as np


#### Define the quadratic and cross-entropy cost functions

class QuadraticCost(object):

    @staticmethod
    def fn(a, y):
        return 0.5*np.linalg.norm(a-y)**2

    @staticmethod
    def delta(z, a, y):
        """Return the error delta from the output layer."""
        return (a-y) * sigmoid_prime(z)


class CrossEntropyCost(object):

    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))

    @staticmethod
    def delta(z, a, y):
        return a - y

    @staticmethod
    def delta_softmax(z, a, y):
        # print(softmax(a))
        # print("\n")
        return softmax(a) - y

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

#### Main Network class
class Network(object):

    def __init__(self, sizes, mentor, nOfLayerOfMentorToLearn, nOfLayerOfMenteeToLearn, par, cost=CrossEntropyCost):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.default_weight_initializer()
        self.cost=cost
        self.mentor=mentor
        self.mentorLayer=nOfLayerOfMentorToLearn
        self.menteeLayer=nOfLayerOfMenteeToLearn
        self.alpha=par[0]
        self.beta=par[1]
        self.gamma=par[2]

    def default_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)/np.sqrt(x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def large_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights)[:-1]:
            a = sigmoid(np.dot(w, a)+b)

        # Since we use the softmax layer in output
        b = self.biases[-1]
        w = self.weights[-1]
        a = softmax(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda = 0.0,
            evaluation_data=None,
            monitor_evaluation_cost=False,
            monitor_evaluation_accuracy=False,
            monitor_training_cost=False,
            monitor_training_accuracy=False):
        if evaluation_data: n_data = len(evaluation_data)
        n = len(training_data)
        evaluation_cost, evaluation_accuracy = [], []
        training_cost, training_accuracy = [], []

        # Loop for training network
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in xrange(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(
                    mini_batch, eta, lmbda, len(training_data), j)
            print "Epoch %s training complete" % j
            # print("\n\n layer =  " + str(len(self.weights)))
            if monitor_training_cost:
                cost = self.total_cost(training_data, lmbda)
                training_cost.append(cost)
                print "Cost on training data: {}".format(cost)
            if monitor_training_accuracy:
                accuracy = self.accuracy(training_data, convert=True)
                training_accuracy.append(accuracy)
                print "Accuracy on training data: {} / {}".format(
                    accuracy, n)
            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                evaluation_cost.append(cost)
                print "Cost on evaluation data: {}".format(cost)
            if monitor_evaluation_accuracy:
                accuracy = self.accuracy(evaluation_data)
                evaluation_accuracy.append(accuracy)
                print "Accuracy on evaluation data: {} / {}".format(
                    self.accuracy(evaluation_data), n_data)
        return evaluation_cost, evaluation_accuracy, \
            training_cost, training_accuracy

    def update_mini_batch(self, mini_batch, eta, lmbda, n, epoch):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        nabla_term1 = [[0 for col in range(15)] for row in range(10)]
        nabla_term2 = [0 for col in range(10)]

        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w, delta_nabla_term1, delta_nabla_term2 = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            nabla_term1 = [term1 + dterm1 for term1, dterm1 in zip(nabla_term1, delta_nabla_term1)]
            nabla_term2 = [term2 + dterm2 for term2, dterm2 in zip(nabla_term2, delta_nabla_term2)]

        # These are the weights between input and hidden layer
        w = self.weights[0]
        nw = nabla_w[0]
        self.weights[0] = (1 - eta * (lmbda/n)) * w - (eta / len(mini_batch)) * nw

        # These are the weights between hidden and output layer
        w = self.weights[1]
        nw = nabla_w[1]
        term1 = [(self.beta * (epoch + 1)) * nbt * nw for nbt, nw in zip(nabla_term1, nw)]

        self.weights[1] = (1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw + term1

        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights)[:-1]:
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        mentorActivations = self.mentor.getActivations(x, self.mentorLayer)
        diffHidden = mentorActivations - activations[-1 * self.menteeLayer]
        # print("Here is the diff between mentor and mentee in hidden layer : \n\n" + diffHidden + "\n\n")

        # calculate the activation of last layer without sigmoid function
        # because we have to use the softmax instead of sigmoid
        b, w = zip(self.biases, self.weights)[-1]
        z = np.dot(w, activation) + b
        zs.append(z)
        activation = z
        activations.append(activation)

        mentorSoftmax = self.mentor.getSoftMaxOuput(x)
        diffSoftmax = mentorSoftmax - softmax(activations[-1])
        # print("Here is the diff between mentor and mentee in softmax layer : \n\n" + diffSoftmax + "\n\n")

        # backward pass
        # use delta_softmax to apply softmax layer
        delta = (self.cost).delta_softmax(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

        ret1 = self.getTerm1(diffHidden)
        ret2 = self.getTerm2(diffSoftmax, softmax(activations[-1]))

        return (nabla_b, nabla_w, ret1, ret2)

    def getTerm1(self, diffHidden):
        diffMenteeMentor = -1 * diffHidden
        diff = [pow(x, 2) for x in diffHidden]
        tmp = (1 /np.sqrt(sum(diff))) / len(diffHidden)
        return diffMenteeMentor * tmp

    def getTerm2(self, diffSoftmax, outputMenteeSoftmax):
        diffMentorMenteeSoftmax = [pow(x, 2) for x in diffSoftmax]
        a = len(diffSoftmax)
        sum2 = (1 / (np.sqrt( sum(diffMentorMenteeSoftmax) / a)))[0]
        ret = []
        for outputDiff, outputMentee in zip(diffSoftmax, outputMenteeSoftmax):
            ydiff = outputDiff[0]
            outMentee = outputMentee[0]
            cur = sum2 * (float(2)/float(a)) * (ydiff * outMentee * (1 - outMentee))
            ret.append(cur)
        return ret

    def accuracy(self, data, convert=False):
        if convert:
            results = [(np.argmax(self.feedforward(x)), np.argmax(y))
                       for (x, y) in data]
        else:
            results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in data]
        return sum(int(x == y) for (x, y) in results)

    def total_cost(self, data, lmbda, convert=False):
        cost = 0.0
        for x, y in data:
            a = self.feedforward(x)
            if convert: y = vectorized_result(y)
            cost += self.cost.fn(a, y)/len(data)
        cost += 0.5*(lmbda/len(data))*sum(
            np.linalg.norm(w)**2 for w in self.weights)
        return cost

    def save(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()

#### Loading a Network
def load(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net

#### Miscellaneous functions
def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
