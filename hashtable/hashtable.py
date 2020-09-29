class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = capacity
        self.array_size = [None for item in range(self.capacity)]
        self.counter = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        Load factor is the number of item that is store within the array
        """
        return self.counter / self.capacity
        # Your code here


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        fnv_basis = 14695981039346656037
        fnv_prime = 1099511628211
        key = key.encode()
        for byte in key:
            hash = fnv_basis^byte
            hash = hash^fnv_prime

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        byte_array = key.encode()
        for byte in byte_array:
            hash = ((hash * 33) ^ byte) % 0x100000000
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        if self.get_load_factor() > 0.7:
            self.resize(self.capacity * 2)

        index = self.hash_index(key)
        entry = HashTableEntry(key, value)
        self.counter += 1

        if self.array_size[index] == None:
            self.array_size[index] = entry

        else:
            current_node = self.array_size[index]
            while current_node != None:
                if current_node.key == key:
                    current_node.value == value
                elif current_node.next == None:
                    current_node.next = entry
                current_node = current_node.next
    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        if self.get(key):
            index = self.hash_index(key)
            current_node = self.array_size[index]
            prev_entry = None
        else:
            print('ValueError: There is no value to delete!')

        while current_node != None:
            if current_node.key == key:
                self.counter -=1
                if prev_entry == None:
                    current_node.value = None
                else:
                    prev_entry = current_node.next
            prev_entry = current_node
            current_node = current_node.next
        
        if self.get_load_factor() < 0.2:
            new_capacity = self.capacity // 2
            if new_capacity < MIN_CAPACITY:
                self.resize(MIN_CAPACITY)
            else:
                self.resize(new_capacity)

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        entry = self.array_size[index]
        if entry is None:
            return None
        while entry != None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        old_array = self.array_size
        self.array_size = [None] * new_capacity
        self.capacity = new_capacity

        for index in range(len(old_array)):
            current_node = old_array[index]
            while current_node != None:
                self.put(current_node.key, current_node.value)
                current_node = current_node.next



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
