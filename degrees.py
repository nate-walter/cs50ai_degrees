import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
# 'kevin bacon': {'102}
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])
    
    #print("Here's you list of movies exdperiment result: ", people[row['id']]['movies'])
    
    #print(names)
    
    # names is populated at this point with all actors

    #print("this is me printing the contents of names", [name for name in names])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }
            

            #"Uncomment to see what this whole 'MOVIES' thing is about"
            # print(movies)
            # print(len(movies))
            # print(movies[row['id']])
            # print(len(movies))
            # print(movies[row['id']]['title'])

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            #print("The line in question in main():", people[path[i + 1][1]]["name"])


def shortest_path(source, target):
    print("you're in shortest_path func")
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    from collections import deque
    # Each item in the queue will be a tuple: (person_id, movie_id they were found by)
    queue = deque([(source, None)])
    visited = set() # Keep track of explored nodes to avoid loops
    previous = {} # A dictionary to remember how we reached each person (which movie and actor led to them)

    while queue:
        person_id, movie_id = queue.popleft()
        print(f"Exploring {person_id=}, through {movie_id=}") # Debug print

        # If this person is the target, then we can exit the BFS loop
        if person_id == target:
            print(f"Found {target}!")
            break
        
        visited.add(person_id)
        
        for m_id, co_actor_id in neighbors_for_person(person_id):
            if co_actor_id not in visited and co_actor_id not in [person[0] for person in queue]:
                queue.append((co_actor_id, m_id))
                if co_actor_id not in previous:
                    previous[co_actor_id] = (person_id, m_id)
                
    # If target was found and added to the previous dict.
    if target in previous:
        path =[]
        current = target
        
        while current != source:
            print(f"previous[641] = {previous.get('641', 'Not found')}")
            print(f"Backtracking: {current=}") # Debug print
            
            person_from, movie_id = previous[current]
            
            path.insert(0, (movie_id, current))
            
            current = person_from
        
        return path
    else:
        return None

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    print("You're in neighbors_for_person")

    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
