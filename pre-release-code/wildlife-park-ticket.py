# task 3


def optimal_tickets(n_seniors: int, n_adults: int, n_children: int):
    out = {}

    # This task is actually a simplified version of a linear optimization
    # problem, as there is a clear precedence for the constraints (e.g. the
    # family ticket is the optimal choice at all times). Also note that the
    # cost for two days is linearly dependent to the cost for one day, thus it
    # does not impose extra constraints or penalty terms to the optimization
    # problem, i.e. the optimal solution for one day would also be the optimal
    # solution for two days.
    #
    # Due to this, the problem can be divided into the following steps:
    # 1. Choose as many family tickets as possible, prioritizing grouping
    #    non-senior adults into the family groups.
    # 2. If the remaining people count is less than 6, then the problem is
    #    trivial, as the optimal purchasing method would be buying individual
    #    tickets.
    # 3. If there are more than 6 adults/seniors remaining, then purchase
    #    group tickets for them and buy tickets for the remaining children
    #    individually; otherwise, buy group tickets for a group of 6 people if
    #    it is a group where the expense of group tickets incurred by the
    #    children is compensated with the reduction by the adults/seniors, and
    #    individually purchase the tickets for the remaining people (e.g.
    #    2 children and 4 seniors for a group ticket would work due to the
    #    constraint (15 - 12) * n_children <= (16 - 15) * n_seniors) + (20 -
    #    15) * n_adults.

    out['family'] = min(n_children // 3, (n_seniors + n_adults) >> 1)
    n_children -= out['family'] * 3
    n_adults -= out['family'] << 1
    if n_adults < 0:
        n_seniors += n_adults
        n_adults = 0

    total = n_seniors + n_adults + n_children
    remain_children = (6 - n_adults - n_seniors)
    if n_seniors + n_adults >= 6:
        out['group'] = n_seniors + n_adults
        out['children'] = n_children
    elif n_adults * 5 + n_seniors >= remain_children * 3 and total >= 6:
        out['group'] = 6
        out['children'] = n_children - remain_children
    else:
        out['seniors'] = n_seniors
        out['adults'] = n_adults
        out['children'] = n_children

    return {k: v for k, v in out.items() if v}


# testing

def price(tickets):
    return tickets.get('family', 0) * 60 + tickets.get('group', 0) * 15 + \
           tickets.get('seniors', 0) * 16 + tickets.get('adults', 0) * 20 + \
           tickets.get('children', 0) * 12


test_data = [(0, 4, 6), (0, 0, 10), (1, 3, 2), (1, 4, 2), (0, 3, 2)]

for i in test_data:
    tickets = optimal_tickets(*i)
    print('price:', price(tickets), '\ttickets:', tickets)
