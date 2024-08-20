
class Tail():
    def __init__(self,file_path,no_of_lines=10,batch_size=2048):
        self.file_path = file_path
        self.no_of_lines = no_of_lines
        self.batch_size = batch_size

    def getLines(self):
        with open(self.file_path, 'rb') as f:
            f.seek(0,2)
            file_size = f.tell()
            lines = []
            batch = b''
            remaining_size = file_size

            while remaining_size > 0 and len(lines) <= self.no_of_lines:
                read_size = min(remaining_size,self.batch_size)
                f.seek(-read_size,1)
                batch += f.read(read_size)
                f.seek(-read_size,1)

                ls = batch.split(b'\n')
                lines += ls
                remaining_size -= read_size
        
        return b'\n'.join(lines[-self.no_of_lines:]).decode('utf-8')


