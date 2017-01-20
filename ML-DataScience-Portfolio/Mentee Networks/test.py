import mnist_loader
import network2
import mentor
import mentee
import network3
from network3 import Network
from network3 import ConvPoolLayer, FullyConnectedLayer, SoftmaxLayer


# Testing network2
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

mentorNet = mentor.load("net.txt")
# mentorNet = mentor.Network([784, 30, 15, 10], cost=mentor.CrossEntropyCost)
# mentorNet.SGD(training_data, 5, 10, 0.1, evaluation_data=test_data, monitor_evaluation_accuracy=True)
# mentorNet.save("net.txt")


print("Start mentee network")
numberOfLayerOfMentorToLearn = 1
numberOfLayerOfMenteeToLearn = 1
menteeNet = mentee.Network([784, 15, 10], mentorNet, numberOfLayerOfMentorToLearn, numberOfLayerOfMenteeToLearn, [1, 0.1,1],cost=mentee.CrossEntropyCost)
menteeNet.SGD(training_data, 30, 10, 0.1, evaluation_data=test_data, monitor_evaluation_accuracy=True, monitor_training_accuracy=True)

print("Comparison")
compareNet = network2.Network([784, 15, 10])
compareNet.SGD(training_data, 20, 10, 0.1, evaluation_data=test_data, monitor_evaluation_accuracy=True, monitor_training_accuracy=True)


# # Testing network2
# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
#
# # net2 = network2.Network([784, 30, 40, 10])
# # net = network2.load("net.txt")
# # print(net.weights[0])
# net = network2.Network([784, 50, 50, 10], cost=network2.CrossEntropyCost)
# # net.large_weight_initializer()
#
# net.SGD(training_data, 100, 10, 0.5, evaluation_data=test_data, monitor_evaluation_accuracy=True)
# net.save("net.txt")




# # Testing network2
# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
#
# # net2 = network2.Network([784, 30, 40, 10])
# # net = network2.load("net.txt")
# # print(net.weights[0])
# net = network2.Network([784, 200, 20, 10], cost=network2.CrossEntropyCost)
# # net.large_weight_initializer()
#
# net.SGD(training_data, 100, 10, 0.1, evaluation_data=test_data, monitor_evaluation_accuracy=True)
# net.save("net.txt")



# Testing network3
# training_data, validation_data, test_data = network3.load_data_shared()
# mini_batch_size = 10
# net = Network([
#     FullyConnectedLayer(n_in=784, n_out=100),
#     FullyConnectedLayer(n_in=100, n_out=100),
#     SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
# net.SGD(training_data, 60, mini_batch_size, 0.1,
#         validation_data, test_data)
# net.save("net3.txt")