# E:
# Creates a hash table and uses chaining as the collision resolution technique
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    """
    Inserts a new item into the hash table. Avg space-time complexity is O(1). Worst case is O(N).
    """

    def insert(self, key, item):
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    """
    Searches for an item with matching key in the hash table. Returns the item if found, or None if not found. 
    Avg space-time complexity is O(1) when all chains are equal length. Worst case is O(N) if all elements are one 
    single linked list. So, the search algorithm must traverse the entire linked list and check every node to yield 
    proper search results.
    """

    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            # find the item's index and return the item that is in the bucket list.
            if kv[0] == key:
                return kv[1]
        return None

    """
    Removes an item with matching key from the hash table. Avg space-time complexity is O(1). Worst case is O(N).
    """

    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
