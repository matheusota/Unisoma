from gurobipy import *
import time

def runModel(instance):
    try:
        # Create a new model
        m = Model("kids_scheduling")

        # Create variables
        x = m.addVars( \
            # kids
            range(len(instance.kids)), \
            # workers
            range(len(instance.workers)), \
            # days
            range(5), \
            # hours
            range(18), \
            vtype=GRB.BINARY, \
            name="x" \
        )

        y = m.addVars(range(len(instance.kids)), vtype=GRB.BINARY, name="y")

        workers_type = [
            "Fonoadiologia", 
            "Terapia Ocupacional",
            "Neurologia",
            "Nutrição",
            "Pedagogia"
        ]

        z = m.addVars( \
            # kids
            range(len(instance.kids)), \
            # workers type
            range(len(workers_type)), \
            # days
            range(5), \
            # period
            range(2), \
            vtype=GRB.BINARY, \
            name="z" \
        )

        v = m.addVars( \
            # kids
            range(len(instance.kids)), \
            # days
            range(5), \
            vtype=GRB.BINARY, \
            name="v" \
        )

        alpha = 0.5

        # Set objective
        m.setObjective(
            quicksum([y[i] for i in range(len(instance.kids))]) + \
            quicksum([-alpha * z[(k, w, d, p)] for k in range(len(instance.kids)) \
                for w in range(len(workers_type)) \
                for d in range(5) \
                for p in range(2)] \
            ), \
            GRB.MAXIMIZE \
        )

        # Add worker availability constraint
        m.addConstrs(((quicksum(x[(k, w, d, h)] for k in range(len(instance.kids))]) <= instance.workers[w][d][h]) \
            for w in range(len(instance.workers)) \
            for d in range(5) \
            for h in range(18)), \
            name = "worker_availability" \
        )

        # Add kid availability constraint
        m.addConstrs(((quicksum(x[(k, w, d, h)] for w in range(len(instance.workers))]) <= instance.kids[k][d][h]) \
            for k in range(len(instance.kids)) \
            for d in range(5) \
            for h in range(18)), \
            name = "kid_availability" \
        )

        # Add z constraints
        m.addConstrs((
            (quicksum(x[(k, w, d, h)] \
                for w in range(len(instance.workers)) \
                for h in range(9))]
            ) <= 200 * z[(k, w, d, 0)]) \
            for k in range(len(instance.kids)) \
            for d in range(5)), \
            name = "z_morning" \
        )

        m.addConstrs((
            (quicksum([x[(k, w, d, h)] \
                for w in range(len(instance.workers)) \
                for h in range(9, 18))]
            ) <= 200 * z[(k, w, d, 1)]) \
            for k in range(len(instance.kids)) \
            for d in range(5)), \
            name = "z_afternoon" \
        )

        # add v constraints
        m.addConstrs(((quicksum([x[(k, w, d, h)] for h in range(18))]) == v[(k, d)]) \
            for k in range(len(instance.kids)) \
            for t in len(workers_type) \
            for d in range(5)), \
            name = "v_constraints" \
        )

        # add periods limit constraints
        m.addConstrs(((z[(k, t, d, 0)] + z[(k, t, d, 1)] <= v[(k, d)]) \
            for k in range(len(instance.kids)) \
            for t in range(len(workers_type)) \
            for d in range(5)), \
            name = "periods_limit" \
        )

        # Add necessary attendaces constraint
        m.addConstrs((
            (quicksum([x[(k, w, d, h)] \
                for d in range(5), \
                for h in range(18), \
                for w in range(len(instance.workers)) \
                if instance.workers[w].type == t]
            ) <= instance.kids.needs[t] * y[k]) \
            for k in range(len(instance.kids)) \
            for t in range(workers_type)), \
            name = "necessary_attendances" \
        )

        # Add days intervals constraints
        m.addConstrs(((quicksum([(1 - v[(k, d)]) for d in range(d1, d2 + 1)) >= v[(k, d1)] + v[(k, d2)] - 1 \
            for d1 in range(5) \
            for d2 in range(d1 + 1, 5) \
            for k in range(len(instance.kids)), \
            name = "day_interval" \
        )

        start_time = time.time()
        m.optimize()

        for k in range(len(instance.kids)):
            for w in range(len(instance.workers)):
                for d in range(5):
                    for h in range(18):
                        if x[(k, w, d, h)].x > 0:
                            print("x[" + str((k, w, d, h)) + "] = " + str(x[(k, w, d, h)].x))
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))