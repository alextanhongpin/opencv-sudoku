
class DLX:
    @staticmethod
    def solve(A):
        torodial = DLX.init_toroidal(A)
        return DLX.search(torodial)

    @staticmethod
    def init_column_labels(A):
        rows, cols = A.shape
        
        # Use a human-readable label.
        labels = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # In case we have a lot of columns...
        if cols >= len(labels):
            labels = list(map(str, range(cols)))

        return labels
    
    @staticmethod
    def init_column_header(A):
        _, cols = A.shape
        labels = DLX.init_column_labels(A)
            
        # The root header links all the column headers.
        root = Y(name='root', 
                 size=float('inf'))
        
        # The column headers is a circular linkedlist.
        curr = root
        for col in range(cols):
            curr.right = Y(name=labels[col])
            curr.right.left = curr
            curr = curr.right

        # Linking the rightmost column label to the root
        # to make it circular.
        curr.right = root
        curr.right.left = curr
        
        return root
    
    @staticmethod
    def header_pointer(root):
        # Simple pointer to help us find the column at constant time.
        header = {}
        curr = root.right
        while curr != root:
            header[curr.name] = curr
            curr = curr.right
        return header
    
    @staticmethod
    def smallest_column_object(root):
        '''
        Attempt to select the column object with the smallest size.
        '''
        curr = root.column.right
        c = root
        while curr != root:
            if curr.size < c.size:
                c = curr
            curr = curr.right
        return c

    @staticmethod
    def init_toroidal(A):
        labels = DLX.init_column_labels(A)
        root = DLX.init_column_header(A)
        header = DLX.header_pointer(root)
        
        for i, row in enumerate(A):
            prev = None
            left = None
            for j, col in enumerate(row):
                if col != 1: continue

                head = header[labels[j]]
                head.size += 1

                curr = head.up
                curr.down = X(column=head,
                              row=i)
                curr.down.up = curr

                curr = curr.down
                curr.down = curr.column
                curr.down.up = curr

                if prev is None:
                    prev = curr
                    prev.right = curr
                    prev.right.left = prev
                    left = curr
                else:
                    prev.right = curr
                    prev.right.left = prev
                    prev = curr

            # Happens when the column does not have any 1s.
            if prev is not None:
                prev.right = left
                prev.right.left = prev
        return root
    
    @staticmethod
    def cover(col):
        col = col.column
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.up.down = j.down
                j.down.up = j.up
                j.column.size -= 1    
                j = j.right
            i = i.down
    
    @staticmethod
    def uncover(col):
        col = col.column
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column.size += 1
                j.up.down = j
                j.down.up = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col
    
    @staticmethod
    def search(root, k=0, solution=None):
        if solution is None:
            solution = []
        if root.right == root:
            return solution[:]

        col = DLX.smallest_column_object(root)
        DLX.cover(col)

        r = col.down
        while r != col:
            o_k = r
            solution.append(o_k.row)

            j = r.right
            while j != r:
                DLX.cover(j)
                j = j.right

            result = DLX.search(root, k+1, solution)
            if result: return result
            solution.remove(o_k.row)

            r = o_k
            col = r.column

            j = r.left
            while j != r:
                DLX.uncover(j)
                j = j.left
            r = r.down
        DLX.uncover(col)
