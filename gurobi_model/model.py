from gurobipy import *
import time

def boolToInt(x):
    if x:
        return 1
    else:
        return 0

def runModel(instance):
    try:
        # Create a new model
        m = Model("kids_scheduling")

        # Create variables
        # x_{k, w, d, h} => kid k got scheduled to worker w in day d and hour h
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

        # y_k => kid k has all the necessary attendances
        y = m.addVars(range(len(instance.kids)), vtype=GRB.BINARY, name="y")

        workers_type = [
            "Fonoadiologia", 
            "Terapia Ocupacional",
            "Neurologia",
            "Nutrição",
            "Pedagogia"
        ]

        # z_{k, t, d, p} => kid k has an attendance of type t in day d and period p
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

        # v_{k, t, d} => kid k has an attendment of type t at day d
        v = m.addVars( \
            # kids
            range(len(instance.kids)), \
            # workers_type
            range(len(workers_type)), \
            # days
            range(5), \
            vtype=GRB.BINARY, \
            name="v" \
        )

        alpha = 0.5

        # Set objective
        m.setObjective(
            quicksum([y[k] for k in range(len(instance.kids))]) + \
            quicksum([-alpha * z[(k, w, d, p)] for k in range(len(instance.kids)) \
                for w in range(len(workers_type)) \
                for d in range(5) \
                for p in range(2)] \
            ), \
            GRB.MAXIMIZE \
        )

        # Add worker availability constraint
        m.addConstrs(((quicksum([x[(k, w, d, h)] for k in range(len(instance.kids))]) <= boolToInt(instance.workers[w].available[d][h])) \
            for w in range(len(instance.workers)) \
            for d in range(5) \
            for h in range(18)), \
            name = "worker_availability" \
        )

        # Add kid availability constraint
        m.addConstrs(((quicksum([x[(k, w, d, h)] for w in range(len(instance.workers))]) <= boolToInt(instance.kids[k].available[d][h])) \
            for k in range(len(instance.kids)) \
            for d in range(5) \
            for h in range(18)), \
            name = "kid_availability" \
        )

        # Add z constraints
        m.addConstrs((
            ((quicksum([x[(k, w, d, h)] \
                for h in range(9) \
                for w in range(len(instance.workers)) \
                if instance.workers[w].type == workers_type[t]])
            ) <= 200 * z[(k, t, d, 0)]) \
            for k in range(len(instance.kids)) \
            for t in range(len(workers_type)) \
            for d in range(5)), \
            name = "z_morning" \
        )

        m.addConstrs((
            ((quicksum([x[(k, w, d, h)] \
                for h in range(9, 18) \
                for w in range(len(instance.workers)) \
                if instance.workers[w].type == workers_type[t]])
            ) <= 200 * z[(k, t, d, 1)]) \
            for k in range(len(instance.kids)) \
            for t in range(len(workers_type)) \
            for d in range(5)), \
            name = "z_afternoon" \
        )

        # add periods limit constraints
        m.addConstrs(((z[(k, t, d, 0)] + z[(k, t, d, 1)] == v[(k, t, d)]) \
            for k in range(len(instance.kids)) \
            for t in range(len(workers_type)) \
            for d in range(5)), \
            name = "periods_limit" \
        )

        # Add necessary attendaces constraint
        m.addConstrs((
            ((quicksum([x[(k, w, d, h)] \
                for d in range(5) \
                for h in range(18) \
                for w in range(len(instance.workers)) \
                if instance.workers[w].type == workers_type[t]])
            ) == instance.kids[k].getAttendanceNumber(workers_type[t]) * y[k]) \
            for k in range(len(instance.kids)) \
            for t in range(len(workers_type))),
            name = "necessary_attendances" \
        )

        # Add days intervals constraints
        m.addConstrs(((quicksum([(1 - v[(k, t, d)]) for d in range(d1, d2 + 1)]) >= v[(k, t, d1)] + v[(k, t, d2)] - 1) \
            for d1 in range(5) \
            for d2 in range(d1 + 1, 5) \
            for t in range(len(workers_type)) \
            for k in range(len(instance.kids))), \
            name = "day_interval" \
        )

        start_time = time.time()
        m.optimize()
        
        for k in range(len(instance.kids)):
            for w in range(len(instance.workers)):
                for d in range(5):
                    for h in range(18):
                        if x[(k, w, d, h)].x > 0.1:
                            print("x[" + str((k, w, d, h)) + "] = " + str(x[(k, w, d, h)].x))
        print()

        for k in range(len(instance.kids)):
            if y[k].x > 0.1:
                print("y[" + str(k) + "] = " + str(y[k].x))
        print()

        for k in range(len(instance.kids)):
            for t in range(len(workers_type)):
                for d in range(5):
                    for p in range(2):
                        if z[(k, t, d, p)].x > 0.1:
                            print("z[" + str((k, t, d, p)) + "] = " + str(z[(k, t, d, p)].x))
        print()
        
        for k in range(len(instance.kids)):
            for t in range(len(workers_type)):
                for d in range(5):
                    if v[(k, t, d)].x > 0.1:
                        print("v[" + str((k, t, d)) + "] = " + str(v[(k, t, d)].x))
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))