import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

def CalcularResultats():

    statistics = open('statistics.json')

    experiments = json.load(statistics)
    statistics.close()

    total_times_experiments = []
    queue_times_experiments = []
    unified_queue_times_experiments = []
    specific_queues_times_experiments = []
    people_in_the_unified_queue = []
    people_in_the_specific_queues = []
    end_time = 0
    time_by_time_people_in_the_unified_queue_exps = []
    time_by_time_people_in_the_specific_queues_exps = []

    for experiment in experiments:
        total_times_experiment = []
        queue_times_experiment = []
        unified_queue_times_experiment = []
        specific_queues_times_experiment = []
        time_by_time_people_in_the_unified_queue_exp = [0] * 100000
        time_by_time_people_in_the_specific_queues_exp = [0] * 100000
        for entity in experiment['entities']:
            total_times_experiment.append(entity['tempsSortida'] - entity['tempsArribada'])
            queue_times_experiment.append(entity['tempsIniciServei'] - entity['tempsArribadaCua'])
            if entity['cua'] == "cua_unica":
                unified_queue_times_experiment.append(entity['tempsIniciServei'] - entity['tempsArribadaCua'])
                people_in_the_unified_queue.append({"start":entity['tempsArribadaCua'], "end":entity['tempsIniciServei']})
                if len(time_by_time_people_in_the_unified_queue_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])]) >= 1:
                    time_by_time_people_in_the_unified_queue_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])] = map(lambda x:x+1,time_by_time_people_in_the_unified_queue_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])])
            else:
                specific_queues_times_experiment.append(entity['tempsIniciServei'] - entity['tempsArribadaCua'])
                people_in_the_specific_queues.append({"start":entity['tempsArribadaCua'], "end":entity['tempsIniciServei']})
                if len(time_by_time_people_in_the_specific_queues_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])]) >= 1:
                    time_by_time_people_in_the_specific_queues_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])] = map(lambda x: x + 1,time_by_time_people_in_the_specific_queues_exp[int(entity['tempsArribadaCua']):int(entity['tempsIniciServei'])])
            if end_time < entity['tempsIniciServei']:
                end_time = entity['tempsIniciServei']
        total_times_experiments.append(total_times_experiment)
        queue_times_experiments.append(queue_times_experiment)
        unified_queue_times_experiments.append(unified_queue_times_experiment)
        specific_queues_times_experiments.append(specific_queues_times_experiment)

        time_by_time_people_in_the_unified_queue_exps.append(time_by_time_people_in_the_unified_queue_exp[:int(end_time)].copy())
        time_by_time_people_in_the_specific_queues_exps.append(time_by_time_people_in_the_specific_queues_exp[:int(end_time)].copy())

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals al supermercat per experiment')
    ax1.boxplot(total_times_experiments)
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals al supermercat mitjana total')
    ax1.boxplot(list(chain.from_iterable(total_times_experiments)))
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a les cues per experiment')
    ax1.boxplot(queue_times_experiments)
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a les cues mitjana total')
    ax1.boxplot(list(chain.from_iterable(queue_times_experiments)))
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a la cua unificada per experiment')
    ax1.boxplot(unified_queue_times_experiments)
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a la cua unificada mitjana total')
    ax1.boxplot(list(chain.from_iterable(unified_queue_times_experiments)))
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a les cues específiques per experiment')
    ax1.boxplot(specific_queues_times_experiments)
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Temps totals a les cues específiques mitjana total')
    ax1.boxplot(list(chain.from_iterable(specific_queues_times_experiments)))
    plt.show()

    for i in time_by_time_people_in_the_unified_queue_exps:
        numbers = [x for x in range(0, len(i))]
        plt.plot(numbers, i)
    plt.title("Nombre de persones a la cua única")
    plt.show()

    for i in time_by_time_people_in_the_specific_queues_exps:
        numbers = [x for x in range(0, len(i))]
        plt.plot(numbers, i)
    plt.title("Nombre de persones a les cues específiques")
    plt.show()

    max_time_unified = max(map(len,time_by_time_people_in_the_unified_queue_exps))
    for i in range(len(time_by_time_people_in_the_unified_queue_exps)):
        time_by_time_people_in_the_unified_queue_exps[i] += [0] * (max_time_unified - len(time_by_time_people_in_the_unified_queue_exps[i]))
    time_by_time_people_in_the_unified_queue_exps_average = [0] * max_time_unified
    for i in range(max_time_unified):
        for x in time_by_time_people_in_the_unified_queue_exps:
            time_by_time_people_in_the_unified_queue_exps_average[i] += x[i]
    time_by_time_people_in_the_unified_queue_exps_average = [x/len(time_by_time_people_in_the_unified_queue_exps) for x in time_by_time_people_in_the_unified_queue_exps_average]

    max_time_specific = max(map(len, time_by_time_people_in_the_specific_queues_exps))
    for i in range(len(time_by_time_people_in_the_specific_queues_exps)):
        time_by_time_people_in_the_specific_queues_exps[i] += [0] * (
                    max_time_specific - len(time_by_time_people_in_the_specific_queues_exps[i]))
    time_by_time_people_in_the_specific_queues_exps_average = [0] * max_time_specific
    for i in range(max_time_specific):
        for x in time_by_time_people_in_the_specific_queues_exps:
            time_by_time_people_in_the_specific_queues_exps_average[i] += x[i]
    time_by_time_people_in_the_specific_queues_exps_average = [x / len(time_by_time_people_in_the_specific_queues_exps) for
                                                             x in time_by_time_people_in_the_specific_queues_exps_average]


    numbers = [x for x in range(0, max(max_time_unified, max_time_specific))]
    plt.plot(numbers, time_by_time_people_in_the_unified_queue_exps_average, label = "Cua Única")
    plt.plot(numbers, time_by_time_people_in_the_specific_queues_exps_average, label = "Cues específiques")
    plt.title("Nombre de persones a la cua única de mitjana")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    CalcularResultats()



