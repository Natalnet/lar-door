from controller.rfidcontroller import RFiDController as rc

import ujson, time

rc = rc()

class DatabaseController:
    
    def __init__(self):
        print('Database controller handled')
        
        try:
            
            archive = open('ID.json').read()
            
            load_archive = ujson.loads(archive)
            load_archive[0]['id']
            
        except:
            
            print('Database is requesting a master card!')
            
            archive = open('ID.json', 'w')
            
            while True:
                
                time.sleep_ms(100)
                
                masterId = str(rc.get())
                
                if masterId != 'no-tag':
                    break
                
            data = [{'id': masterId, 'name':'Master'}]
                
            archive.write(ujson.dumps(data))
            archive.close()
                
    def findcard(self, tag):
        
        archive = open('ID.json').read()
        
        load_archive = ujson.loads(archive)
        
        amount = int(len(load_archive))
        
        findTag = tag
        
        for i in range(amount):
            
            if load_archive[i]['id'] == findTag:
                return (True, i)
        
        return (False, i)
    
    def findname(self, tag):
        
        archive = open('ID.json').read()
        
        load_archive = ujson.loads(archive)
        
        amout = int(len(load_archive))
        
        findTag = tag
        
        for i in range(amount):
            
            if load_archive[i]['id'] == findTag:
                name = load_archive[i]['name']
                
                return name
            
        return 'no-tag'
    
    def addcard(self, tag, name):
        
        if self.findcard(tag)[0] == False:
            
            archive = open('ID.json').read()
            
            load_archive = ujson.loads(archive)
            
            data = {
                'id':tag,
                'name':name
            }
            
            load_archive.append(data)
            
            archive = open('ID.json', 'w')
            archive.write(ujson.dumps(load_archive))
            archive.close()
            
            print(f'Card {tag} registered on the database')
            
        else:
            
            print('Card already exists on database')
            
    def removecard(self, tag):
        
        pos = int(self.findcard(tag)[1])
        
        archive = open('ID.json').read()
        
        load_archive = ujson.loads(archive)
        load_archive.pop(pos)
        
        archive = open('ID.json', 'w')
        archive.write(ujson.dumps(load_archive))
        archive.close()
        
        print(f'Card {tag} removed from the database')
    
    def ismastercard(self, tag):
        
        archive = open('ID.json').read()
        
        load_archive = ujson.loads(archive)
        
        if load_archive[0]['id'] == tag:
            return True
        else:
            return False
    
    def amount(self):
        
        archive = open('ID.json').read()
        
        load_archive = ujson.loads(archive)
        
        amount = int(len(load_archive))
        
        return amount

