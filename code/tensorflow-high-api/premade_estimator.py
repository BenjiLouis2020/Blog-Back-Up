# -*- coding: utf-8 -*-
# Author: Lawlite
# Date: 2018/05/31
# Associate Blog: 
# License: MIT
import tensorflow as tf
import argparse
import iris_data


# 超参数
parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help="batch size")
parser.add_argument('--train_steps', default=1000, type=int, help="number of training steps")

def main(argv):
    args = parser.parse_args(argv)
    # 加载数据， pandas类型
    (train_x, train_y), (test_x, test_y) = iris_data.load_data()
    # feature columns描述如何使用输入数据
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key = key))
    # 建立模型
    cls = tf.estimator.DNNClassifier(hidden_units=[10,10], feature_columns=my_feature_columns, 
                                    n_classes=3)
    # 训练模型
    cls.train(input_fn=lambda:iris_data.train_input_fn(train_x, train_y, args.batch_size),
              steps=args.train_steps)
    # 评价模型
    eval_res = cls.evaluate(input_fn=lambda:iris_data.eval_input_fn(test_x, test_y, args.batch_size))
    print("\n Test Set accuracy: {:0.3f}\n".format(eval_res['accuracy']))
    
    # 预测
    expected = ['Setosa', 'Versicolor', 'Virginica']
    predict_x = {
        'SepalLength': [5.1, 5.9, 6.9],
        'SepalWidth':  [3.3, 3.0, 3.1],
        'PetalLength': [1.7, 4.2, 5.4],
        'PetalWidth':  [0.5, 1.5, 2.1],        
    }
    
    predictions = cls.predict(input_fn=lambda:iris_data.eval_input_fn(predict_x, 
                                                                      labels=None,
                                                                      batch_size=args.batch_size))
    template = ('\n Prediction is "{}" ({:.1f}%), expected "{}"' )
    for pred_dict, expec in zip(predictions, expected):
        class_id = pred_dict['class_ids'][0]
        prob = pred_dict['probabilities'][class_id]
        print(template.format(iris_data.SPECIES[class_id], 100*prob, expec))
        
if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main=main)
    