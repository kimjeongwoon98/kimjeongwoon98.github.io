def pre_processing(image_pixel, distance=4):
    #밝기값이 유사한 픽셀들을 하나의 그룹으로 분류하고 그룹 내의 어느 한 객체의 밝기값으로 다른 픽셀의 것을 수정하는 함수다.
    #input parameter 총 2개로 image_pixel는 image의 각 픽셀의 밝기값을 저장하고 있으며, distance는 두 픽셀의 밝기값이 유사하도고 할 수 있는 허용치이다.
    #만약 input parameter가 각 픽셀의 밝기값을 저장하는 2D array가 아니고 RGB 정보를 각 픽셀마다 저장하면, 픽셀의 각 RGB 성분에 대한 평균을 구한다.
    #출력 파라미터는 각 픽셀에 대한 밝기값과 픽셀이 속한 그룹에 대한 정보를 저장한 리스트다. 밝기값은 특정 픽셀이 분류된 그룹의 한 객체의 밝기값이다.
    #출력 파라미터에서 각 픽셀의 밝기값을 저장하지 않고 그룹 index만 저장해도 edges로 분류할 수 있다. 그래서 픽셀의 정보를 활용하지 않고 그룹 index만을 사용하고 싶으면 get_edges의 image_pixel[i][j][1]를 image_pixel[i][j]로 수정하여 연산비용을 줄일 수 있다.
    #box-filter와 가우시안 필터처럼 스무딩(smoothing)을 하는 작업이지만 두 방법과 달리 특정 모형을 전재로 하지 않기 때문에 유연성이 이전보다 높다
    #이로 인해 box와 가우시안 필터로 인해 발생하는 편차를 줄일 수 있다. 그리고 이 전처리는 픽셀의 RGB와 밝기값이 확률변수이지만 동일한 조건에서 큰 차이가 없다는 것을 전재로 하고 있다.    
    
    result=[] #데이터 변화한 결과물로, 파이썬에서는 리스트를 shallow copy하기 때문에 이로 인한 메모리 침범을 방지하고자 따로 결과물을 저장한다.
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(0, len(image_pixel), 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다. for문에서 이를 사용해서 불필요한 반복연산을 방지하고자 한다.
    
    for i in row_index: #입력파라미터와 동일한 픽셀 갯수를 만들고자 한다.
        result.append([])
        for j in column_index:
            result[i].append([])

    
    for i in row_index: #image_pixel의 각 픽셀마다 어느 그룹에 속하는가를 정할 수 있도록 하기 위해, 그에 맞는 데이터 구조를 설정한다.
        for j in column_index: #각 픽셀은 매우 작은 메모리가 할당되어서 저장되었으며, 이로 인한 overflow가 발생하는 것을 방지하기 위해 정수타입으로 값을 저장한다.
            try: #각 픽셀의 밝기값을 저장했다면 try 구문을 수행하고, 각 픽셀의 RGB 정보를 처리하면 except 구문에서 RGB 평균을 구하고 이를 저장한다.
                temp=int(image_pixel[i][j]) #파이썬의 리스트를 잘못 사용하면 데이터 침범이 발생할 수 있기 때문에 이를 방지하고자 변수로 값을 할당한다.
            except: #opencv는 정수에 대한 메모리를 작게 설정했기 떄문에 이로 인한 overflow를 방지하기 위해, 정수타입으로 변환하고 연산을 수행한다.
                temp=int(int(image_pixel[i][j][0])+int(image_pixel[i][j][1])+int(image_pixel[i][j][2]))/3
            result[i][j]=[temp, -1] #-1은 해당 픽셀이 분류되지 않았음을 의미한다.
    
    temp=result[0][0][0]
    result[0][0]=[temp, 0] #(0,0) pixel은 0번째 그룹에 속한다고 정의한다.
    
    group=[int(result[0][0][0])] #특정 픽셀을 기준으로 비슷한 것을 분류하는 작업을 수행할 것이다. 좌표 (0,0) 픽셀과 밝기가 유사한 픽셀들의 집합을 0번째 그룹으로 한다.
    for i in row_index: #픽셀들을 밝기값이 유사한 것끼리 모으고 있다. i는 i번재 행을 의미한다(i는 정수).
        for j in column_index: #j는 j번째 열을 의미한다(j는 정수).
            group_index=0 #픽셀이 분류될 그룹 index
            group_len=len(group) #그룹의 개수
            min_distance_pixel_group=abs(result[i][j][0]-group[0])#특정 픽셀을 그룹으로 분류하기 위해 우선 초기값을 결정해야 한다.
            
            for l in range(0, group_len, 1): #픽셀과 그룹간 밝기값의 차이가 가장 작은 그룹을 찾고 반복문이다.
                if (abs(group[l]-result[i][j][0])<min_distance_pixel_group): 
                    min_distance_pixel_group=abs(group[l]-result[i][j][0])
                    group_index=l
                    
            if(abs(group[group_index]-result[i][j][0])<distance): #픽셀과 그룹간 밝기차가 기준치 distance보다 작으면 해당 픽셀을 그 그룹으로 분류한다.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #픽셀과 그룹간 밝기차가 기준치 distance보다 작으면 해당 픽셀을 그 그룹으로 분류한다.
                group.append(result[i][j][0]) #새로운 그룹을 추가한다.
                result[i][j][1]=len(group) #len를 index로 취한다는 것은 새롭게 추가한 그룹의 index를 취한다는 것을 의미한다.
    return result

def determine_distance(image_pixel):
    #input parameter 총 1개로 image_pixel는 image의 각 픽셀의 밝기값을 저장하고 있다.
    #이 함수는 이미지 밝기값의 평균을 구하고 이를 각 픽셀의 밝기값에 뺀다. 이후 밝기값을 나열함으로써 순서통계량을 구할 수 있는데, 평균으로부터 멀어진 정도가 통계적으로 0.95만큼 유의미한 두 값(p-value)을 구한다.
    #그리고 두 값을 distance라고 할 것인데, canny edges dectector에서 threshold와 같은 역할을 한다.
    #이 함수는 pre_processing에서 distnace를 통계적으로 결정하는데 사용될 수 있다.
    #출력 파라미터는 두개의 distance와 평균을 뺀 밝기값의 중앙값이다. 중앙값은 차후 threshold를 3개 사용하고자 하는 사용자를 위해 반환하고 있다.
        
    distribution=[] #각 픽셀의 밝기값을 모두 저장한 리스트로, 이를 통해 평균을 구한 다음 각 원소에 평균을 빼서 분포를 추정하고자 한다.
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(0, len(image_pixel), 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다.
    
    for i in row_index: #픽셀은 매우 작은 메모리가 할당되어서 저장되었으며, 이로 인한 overflow가 발생하는 것을 방지하기 위해 정수타입으로 값을 저장한다.
        for j in column_index:
            try: #흑백 이미지를 기준으로 처리하기 때문에 컬리 이미지를 파라미터로 받으면 오류가 발생한다.
                temp=int(image_pixel[i][j]) #리스트를 참조해서 발생하는 메모리 침범을 방지하고자 임시변수를 사용한다.
                distribution.append(temp)
            except:
                temp=(int(image_pixel[i][j][0])+int(image_pixel[i][j][1])+int(image_pixel[i][j][2]))/3
                distribution.append(temp)
            
    distribution_size=len(distribution); distribution_mean=sum(distribution)/distribution_size #이미지의 평균 밝기를 구한다.
    for i in range(0,distribution_size,1): #distribution에 있는 객체에 평균을 빼고자 한다.
        temp=abs(distribution[i]-distribution_mean) #거리의 분포를 보고 있기 때문에 절댓값을 취해야 한다.
        distribution[i]=temp
    
    distribution.sort() #얻은 결과를 오름차순으로 정렬한다. 이를 통해 평균으로부터 떨어져 있어 나올 확률이 0.05와 0.95에 해당되는 값을 쉽게 구할 수 있다.
    stastic_095=0; stastic_005=0 #stastic_095은 중앙값보다 큰 값 중 나올 확률이 0.05이하가 되는 p-value다. stastic_005은 중앙값보다 작은 값 중 나올 확률이 0.05이하가 되는 p-value다.
    
    for i in range(0,distribution_size,1): #평균으로부터 떨어질 확률이 0.05에 해당되는 index를 구하고 이에 대응되는 값을 구한다.
        if((i/distribution_size<=0.05) and (((i+1)/distribution_size>0.05))): #i번째 때는 확률이 0.05보다 작지만 i+1번째는 확률이 0.05보다 크다는 것은 누적분포함수가 연속이기 때문에 중간값정리로 인해 i와 i+1번째 사이에는 0.05를 만족하는 index가 존재해야 한다. 하지만 지금은 이산 데이터를 다루고 있기 때문에 근사로 i번째 값을 취한다.
            stastic_005=abs(distribution[i]) #하지만 지금은 이산 데이터를 다루고 있기 때문에 근사로 i번째 값을 취한다.또한 거리를 구하기 때문에 절대값을 취해야 한다.
            break #더 이상 반복문을 수행할 필요가 없기 때문에 중단한다.
            
    for i in range(distribution_size-1, -1, -1): #평균으로부터 떨어질 확률이 0.95에 해당되는 index를 구하고 이에 대응되는 값을 구한다.
        if((i/distribution_size>=0.95) and (((i-1)/distribution_size<0.95))): #i번째 때는 확률이 0.95보다 크지만 i-1번째는 확률이 0.95보다 크다는 것은 누적분포함수가 연속이기 때문에 중간값정리로 인해 i와 i+1번째 사이에는 0.95를 만족하는 index가 존재해야 함을 의미한다. 하지만 지금은 이산 데이터를 다루고 있기 때문에 근사로 i번째 값을 취한다.
            stastic_095=abs(distribution[i]) #거리를 구하기 때문에 절대값을 취해야 한다.
            break #더 이상 반복문을 수행할 필요가 없기 때문에 중단한다.
    
    median=abs(distribution[int(distribution_size/2)]) #중앙값을 얻는다.
    return [stastic_005, median, stastic_095]

def pre_processing_color(image_pixel, correlation=0.8):
    #input parameter 총 2개로 image_pixel는 image의 각 픽셀의 RGB값을 저장하고 있으며, correlation RGB 공간에서 두 벡터를 같은 그룹으로 분류하기 위한 유사도이다.
    #pre_processing에서는 픽셀들의 밝기값 차이가 특정 임계치보다 작으면 같은 그룹으로 분류했는데, 여기서는 RGB공간에서 특정 픽셀과 그룹의 대표값간의 벡터의 내적을 구하고 그 값이 correlation보다 크면 같은 그룹으로 분류한다.
    #출력 파라미터는 각 픽셀에 대한 RGB값과 픽셀이 속한 그룹에 대한 정보를 저장한 리스트다.
    #pre_processing이 밝기값이 유사한 상황에서는 성능이 좋지 못한다는 문제점을 가지고 있으며, 이를 극복하기 위해 여기서는 color 정보를 직접 활용한다.
    #그리고 이 전처리는 픽셀의 RGB가 동일한 조건에서 큰 차이가 없다는 것을 전재로 하고 있다.    
    
    result=[] #데이터 변화한 결과물로, 파이썬에서는 리스트를 shallow copy하기 때문에 이로 인한 메모리 침범을 방지하고자 따로 결과물을 저장한다.
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(0, len(image_pixel), 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다. for문에서 이를 사용해서 불필요한 반복연산을 방지하고자 한다.
    
    for i in row_index: #입력파라미터와 동일한 픽셀 갯수를 만들고자 한다.
        result.append([])
        for j in column_index:
            result[i].append([])
    
    for i in row_index: #image_pixel의 각 픽셀마다 어느 그룹에 속하는가를 정할 수 있도록 하기 위해, 그에 맞게 데이터 구조를 설정한다.
        for j in column_index:
            #opencv에서는 RGB값을 메모리가 매우 작은 정수타입으로 저장하고 있다. 그래서 큰 값을 연산할 때 overflow가 발생하기 때문에 이를 방지하고자 메모리가 큰 int를 사용한다.
            temp=[int(image_pixel[i][j][0]),int(image_pixel[i][j][1]), int(image_pixel[i][j][2])]  #파이썬의 리스트를 잘못 사용하면 데이터 침범이 발생할 수 있기 때문에 이를 방지하고자 변수로 값을 할당한다.
            result[i][j]=[temp, -1] #-1은 해당 픽셀이 분류되지 않았음을 의미한다.
    
    temp=result[0][0][0]
    result[0][0]=[temp, 0] #(0,0) pixel은 0번째 그룹에 속한다고 정의한다.
    
    group=[result[0][0][0]] #특정 픽셀을 기준으로 비슷한 것을 분류하는 작업을 수행할 것이다. 좌표 (0,0) 픽셀과 각각의 RGB가 유사한 픽셀들의 집합을 0번째 그룹으로 한다.
    for i in row_index: #RGB공간에서 각 픽셀과 그룹의 대표 객체간의 내적을 구하고, 그 결과가 임계치를 넘으면 같은 그룹으로 분류하고 그렇지 않으면 해당 픽셀을 새로운 그룹의 대표 객체로 선언한다.
        for j in column_index: #i는 i번재 행을 의미한다(i는 정수). j는 j번째 열을 의미한다(j는 정수).
            group_index=0 #픽셀이 분류될 그룹 index
            group_len=len(group) #그룹의 개수
            
            #아래 3줄은 0번째 group의 대표 객체와 해당 (i,j)의 객체간 RGB 공간에서의 내적을 구한다. 이는 다른 그룹의 것과 비교하기 위한 초기값 역할을 한다.
            group_object_size=(group[0][0]**2+group[0][1]**2+group[0][2]**2)**(0.5) #0번째 group의 대표값의 유클리드 크기
            pixel_size=(result[i][j][0][0]**2+result[i][j][0][1]**2+result[i][j][0][2]**2)**(0.5) #pixel의 유클리드 크기
            product=(group[0][0]*result[i][j][0][0])+(group[0][1]*result[i][j][0][1])+(group[0][2]*result[i][j][0][2])#0번째 group의 대표값과 pixel간의 내적
            
            try:
                max_correlation=(product)/(group_object_size*pixel_size) #특정 픽셀을 그룹으로 분류하기 위해 우선 초기값을 결정해야 한다.
            except:
                max_correlation=0 #pixel_size가 0이면 오류가 발생한 것이고, 이는 해당 픽셀이 원점에 있다는 것을 의미하기 때문에 0으로 할당해도 무방하다.
            
            #RGB공간에서 두 벡터의 유사도가 기준치 correlation보다 크면 같은 그룹으로 분류할 것이다. RGB공간에서는 모든 값들이 양수만을 갖기 때문에 내적이 음수일 경우는 없다.
            for l in range(0, group_len, 1): #픽셀과 그룹간 상관관계가 가장 큰 그룹을 찾고 있는 반복문이다.
                try:
                    group_object_size=(group[l][0]**2+group[l][1]**2+group[l][2]**2)**(0.5) #l번째 group의 대표값의 유클리드 크기
                    product=(group[l][0]*result[i][j][0][0])+(group[l][1]*result[i][j][0][1])+(group[l][2]*result[i][j][0][2])#0번째 group의 대표값과 pixel간의 내적
                    compare_correlation=product/(group_object_size*pixel_size)#l번째 group의 대표값과 (i,j) 픽셀간 내적
                except:
                    compare_correlation=0 #여기서도 pixel_size가 0이면 오류가 발생한 것이고, 이는 해당 픽셀이 원점에 있다는 것을 의미하기 때문에 0으로 할당해도 무방하다.
                
                if (compare_correlation>max_correlation): #특정 픽셀과 유사도가 가장 높은 그룹을 찾고 있다.
                    max_correlation=compare_correlation
                    group_index=l
            
            if(max_correlation>correlation): #픽셀과 그룹간 상관관계가 기준치보다 높으면 해당 픽셀을 그룹으로 분류한다.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #픽셀과 그룹간 밝기차가 기준치 distance보다 작으면 해당 픽셀을 그 그룹으로 분류한다.
                group.append(result[i][j][0]) #새로운 그룹을 추가한다.
                result[i][j][1]=len(group) #len를 index로 취한다는 것은 새롭게 추가한 그룹의 index를 취한다는 것을 의미한다.
    return result

def pre_processing_total(image_pixel, correlation=0.8):
    #input parameter 총 2개로 image_pixel는 image의 각 픽셀의 RGB값을 저장하고 있으며, correlation은 RGBL(RGB+밝기값을 포함한 공간)공간에서 두 벡터를 같은 그룹으로 분류할 수 있는 기준이다.
    #pre_processing_color은 RGB를 기준으로 픽셀을 특정 그룹으로 분류했는데, 여기서는 RGB에 밝기값 정보를 추가해서 4차원 공간에서 특정 픽셀과 그룹의 대표 객체 간의 벡터의 내적을 구하고 그 값이 correlation보다 크면 같은 그룹으로 분류한다.
    #출력 파라미터는 각 픽셀에 대한 RGBL(L은 해당 픽셀의 밝기값)값과 픽셀이 속한 그룹에 대한 정보를 저장한 리스트다.
    #pre_processing_color에서는 RGB만을 고려하기 떄문에 픽셀들의 밝기값 차이가 있음에도 불구하고 색깔이 비슷해서 edges로 분류하지 못한 상황이 발생할 수 있다. 이 함수는 이를 극복하기 위해 RGB와 밝기값 정보를 동시에 활용한다.
    #그리고 이 전처리는 픽셀의 RGB가 동일한 조건에서 큰 차이가 없다는 것을 전재로 하고 있다.    
    
    result=[] #데이터 변화한 결과물로, RGB가 아닌 RGBL으로 4차원 데이터를 저장하고 있기 때문에 이미지를 표현할 때 주의해야 한다.
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(0, len(image_pixel), 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다. for문에서 이를 사용해서 불필요한 반복연산을 방지하고자 한다.
    
    for i in row_index: #입력파라미터와 동일한 픽셀 갯수를 만들고자 한다.
        result.append([])
        for j in column_index:
            result[i].append([])
    
    for i in row_index: #image_pixel의 각 픽셀마다 어느 그룹에 속하는가를 정할 수 있도록 하기 위해, 그에 맞는 데이터 구조를 설정한다.
        for j in column_index:
            #opencv에서는 RGB값을 메모리가 매우 작은 정수타입으로 저장하고 있다. 그래서 큰 값을 연산할 때 overflow가 발생하기 때문에 이를 방지하고자 메모리가 큰 int를 사용한다.
            temp=[int(image_pixel[i][j][0]),int(image_pixel[i][j][1]), int(image_pixel[i][j][2])] #파이썬의 리스트를 잘못 사용하면 데이터 침범이 발생할 수 있기 때문에 이를 방지하고자 변수로 값을 할당한다.
            temp.append(int(sum(temp)/3)) #기존 RGB공간에 밝기값을 추가한 4차원 공간을 만들고자 한다.
            result[i][j]=[temp, -1] #-1은 해당 픽셀이 분류되지 않았음을 의미한다.
    
    temp=result[0][0][0]
    result[0][0]=[temp, 0] #(0,0) pixel은 0번째 그룹에 속한다고 정의한다.
    
    group=[result[0][0][0]] #특정 픽셀을 기준으로 비슷한 것을 분류하는 작업을 수행할 것이다. 좌표 (0,0) 픽셀과 각각의 RGBL이 유사한 픽셀들의 집합을 0번째 그룹으로 한다.
    for i in row_index:
        for j in column_index: #j는 j번째 열을 의미한다(j는 정수).
            group_index=0 #픽셀이 분류될 그룹 index
            group_len=len(group) #그룹의 개수
            
            group_object_size=(group[0][0]**2+group[0][1]**2+group[0][2]**2+group[0][3]**2)**(0.5) #0번째 group의 대표값의 유클리드 크기
            pixel_size=(result[i][j][0][0]**2+result[i][j][0][1]**2+result[i][j][0][2]**2++result[i][j][0][3]**2)**(0.5) #pixel의 유클리드 크기
            product=(group[0][0]*result[i][j][0][0])+(group[0][1]*result[i][j][0][1])+(group[0][2]*result[i][j][0][2])+(group[0][3]*result[i][j][0][3])#0번째 group의 대표값과 pixel간의 내적
            
            try:
                max_correlation=(product)/(group_object_size*pixel_size) #특정 픽셀을 그룹으로 분류하기 위해 우선 초기값을 결정해야 한다.
            except:
                max_correlation=0 #pixel_size가 0이면 오류가 발생한 것이고, 이는 해당 픽셀이 원점에 있다는 것을 의미하기 때문에 0으로 할당해도 무방하다.
            
            #RGB공간에서 두 벡터의 유사도가 기준치 correlation보다 큰 그룹으로 분류할 것이다. RGBL공간에서는 모든 값들이 양수만을 갖기 때문에 내적이 음수일 경우는 없다.
            for l in range(0, group_len, 1): #픽셀과 그룹간 상관관계가 가장 크고 밝기값의 차이가 가장 작은 그룹을 찾고 있는 반복문이다.               
                try:
                    group_object_size=(group[l][0]**2+group[l][1]**2+group[l][2]**2+group[l][3]**2)**(0.5) #l번째 group의 대표값의 유클리드 크기
                    product=(group[l][0]*result[i][j][0][0])+(group[l][1]*result[i][j][0][1])+(group[l][2]*result[i][j][0][2])+(group[l][3]*result[i][j][0][3])#0번째 group의 대표값과 pixel간의 내적
                    compare_correlation=product/(group_object_size*pixel_size)#l번째 group의 대표값과 (i,j) 픽셀간 내적
                except:
                    compare_correlation=0 #여기서도 pixel_size가 0이면 오류가 발생한 것이고, 이는 해당 픽셀이 원점에 있다는 것을 의미하기 때문에 0으로 할당해도 무방하다.
                
                if (compare_correlation>max_correlation): #특정 픽셀과 유사도가 가장 높은 그룹을 찾고 있다.
                    max_correlation=compare_correlation
                    group_index=l
            
            if(max_correlation>correlation): #픽셀과 그룹간 상관관계가 기준치보다 높으면 해당 픽셀을 그룹으로 분류한다.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #픽셀과 그룹간 밝기차가 기준치 distance보다 작으면 해당 픽셀을 그 그룹으로 분류한다.
                group.append(result[i][j][0]) #새로운 그룹을 추가한다.
                result[i][j][1]=len(group) #len를 index로 취한다는 것은 새롭게 추가한 그룹의 index를 취한다는 것을 의미한다.
    return result

def get_edges(image_pixel):
    #input parameter 총 1개로 image_pixel은 픽셀에 대한 정보를 리스트 형식으로 저장하고 있는데, 여기서 정보는 해당 픽셀에서의 RGB정보와 픽셀이 분류되는 그룹 index에 대한 리스트를 말한다.
    #출력 파라미터는 각 픽셀이 edges인가에 대한 정보를 담고 있는 리스트다. 해당 픽셀이 edges면 255 그렇지 않으면 0을 각 픽셀이 가지고 있다. 0과 1로 값을 넣어도 되지만 결과물을 편하게 출력하기 위해 0과 255로 edges 여부를 표기한다.
    #해당 픽셀과 양옆의 픽셀 또는 위아래의 픽셀과의 그룹을 비교하고, 두 가지 경우 중 최소 하나에 대해 다른 그룹이 존재한다고 판단되면 해당 픽셀을 edges라고 판단할 것이다.
    #이전 pre_processing에서 픽셀들을 이미 그룹으로 분류했기 때문에 사용할 수 있으며, 기존 방식과 달리 덧셈과 곱셈 연산을 수행하지 않아 속도가 빠를 수 있다.
    
    result=[] #각 픽셀의 edges인가를 0(edges가 아니다)와 255(edges가 맞다)으로 각 픽셀마다 저장하는 리스트이며, 이를 반환할 예정이다. 리스트는 기본적으로 shallow copy이기 때문에, 메모리 침범을 방지하고자 따로 리스트를 만들고자 한다.
    row_index_forgenerating=list(range(0, len(image_pixel), 1)) #result를 생성하기 위한 index 
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(1, len(image_pixel)-1, 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다. 첫번째와 마지막 행은 따로 처리하기 때문에 이들은 제외한다.
    
    for i in row_index_forgenerating: #image_pixel은 각 픽셀의 밝기값과 픽셀이 속한 그룹을 가지고 있기 때문에, edges만을 저장하도록 데이터 구조를 정의한다. 
        result.append([])
        for j in column_index:
            result[i].append(0)
    del row_index_forgenerating #더 이상 필요없기 때문에 메모리를 절약하기 위해 삭제한다.
    
    for i in column_index: #첫번째 행과 마지막 행은 모든 방향의 픽셀과 비교할 수 없기 때문에 일부 방향에 대해 픽셀비교를 수행한다.
        try: 
            #아래 if-elif(else if)문은 첫번째 행에 있는 픽셀에 대해서 비교를 수행한다.
            if((image_pixel[0][i][1]!=image_pixel[0][i+1][1]) or (image_pixel[0][i-1][1]!=image_pixel[0][i][1])):
                result[0][i]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            
            #아래 if-elif(else if)문은 마지막 행에 있는 픽셀에 대해서 비교를 수행한다. 파이썬에서는 index가 음수면 마지막에 있는 객체부터 참조한다.
            if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1]) or (image_pixel[-1][i-1][1]!=image_pixel[-1][i][1])):
                 result[-1][i]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                 result[-1][i]=255
                    
        except: #첫번째 열과 마지막열에서는 index를 넘어가는 오류가 있기 때문에 이에 대해서도 별도의 방법으로 픽셀비교를 수행한다.
            if(i==0): #첫번째 열에 대해서는 오른쪽에 있는 픽셀만을 비교할 수 있다.
                if((image_pixel[0][i][1]!=image_pixel[0][i+1][1])):
                    result[0][i]=255 #특정픽셀과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                    result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                
                if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1])):
                    result[-1][i]=255 #특정픽셀과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(column_index[-1][i][1]!=column_index[-2][i][1]):
                    result[-1][i]=255
                    
            else: #첫번째 열 외 오류가 날 수 있는 열은 마지막 열이며, 여기서는 왼쪽에 있는 픽셀만을 비교할 수 있다.
                if((image_pixel[0][i][1]!=image_pixel[0][i-1][1])):
                    result[0][i]=255 #특정픽셀과 왼쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                    result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                
                if((image_pixel[-1][i][1]!=image_pixel[-1][i-1][1])):
                    result[-1][i]=255 #특정픽셀과 왼쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                    result[-1][i]=255
    
    for i in row_index: #위의 반복문에서는 첫번째와 마지막 행에 대해 수행했기 때문에, 여기서는 나머지 행에 대해 edges 여부를 확인하고, edges면 255를 할당한다.
        for j in column_index:
            try: 
                if((image_pixel[i][j][1]!=image_pixel[i][j+1][1]) or (image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                    result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                     result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            
            except: #첫번째 열과 마지막열에서는 index를 넘어가는 오류가 있기 때문에 이에 대해서도 별도의 방법으로 픽셀비교를 수행한다.
                if(i==0): #첫번째 열에 대해서는 오른쪽에 있는 픽셀만을 비교할 수 있다.
                    if((image_pixel[i][j][1]!=image_pixel[i][j+1][1])):
                        result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                         result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    
                else: #첫번째 열 외 오류가 날 수 있는 열은 마지막 열이며, 여기서는 왼쪽에 있는 픽셀만을 비교할 수 있다.
                    if((image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                        result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                        result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
    
    return result

def check_noise_neighborhood(image_pixel,i,j, threshold):
    #(i,j) 픽셀의 neighborhood r개의 그룹을 확인하고, 그룹의 종류와 neighborhood의 비율이 threshold(0과 1사이의 실수)보다 많으면 해당 픽셀을 노이즈라고 판단한다.
    #입력파라미터는 픽셀의 좌표 (i,j)와 임계치인 threshold 및 이미지인 image_pixel이며, 출력파라미터는 bool(0은 (i,j)좌표가 noise라는 것을 의미한다)이다.
    #이는 get_edges_neighborhood에서 사용되기 때문에, 해당 함수에서 사용되는 변수 image_pixel은 get_edges_neighborhood의 입력파라미터이다.
    
    neighborhood=set() #집합은 리스트와 달리 원소를 중복해서 저장하지 않기 때문에, 특정 픽셀의 주변에서 어떤 group으로 분류되었는지를 알 수 있다.
    numberofneighborhood=9 #픽셀의 neighborhood 갯수며, 3x3참조가 가장 많이 이뤄지기 때문에 기본값을 9로 설정함으로써 연산량을 줄일 수 있다.
    if(i==0): #첫 번째 행과 마지막 행은 3x3 주변을 확인하면 index 침범으로 인한 오류가 발생하기 때문에, 6개만의 neighborhood만 확인한다.
        if(j==0): #마찬가지로 첫 번째 열과 마지막 열에서 index 침범이 발생하기 때문에 다른 방식으로 데이터를 저장한다.
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
            numberofneighborhood=4 #해당 픽셀의 주변 중 확인한 것은 4개 밖에 없기 때문에, 값을 수정한다.
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j-1][1])
            numberofneighborhood=4
        else: #첫번째와 마지막 열을 제외한 나머지에서는 좌우, 상하(0번째 행는 하만, 마지막 행은 상만) 방향으로 픽셀을 참조하고 이를 저장할 수 있다.
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j+1][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);  neighborhood.add(image_pixel[i+1][j-1][1]);
            numberofneighborhood=6
    
    elif(i==len(image_pixel)):
        if(j==0): #마찬가지로 첫 번째 열과 마지막 열에서 index 침범이 발생하기 때문에 다른 방식으로 데이터를 저장한다.
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            numberofneighborhood=4
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j-1][1])
            numberofneighborhood=4
        else: #첫번째와 마지막 열을 제외한 나머지에서는 좌우, 상하(0번째 행는 하만, 마지막 행은 상만) 방향으로 픽셀을 참조하고 이를 저장할 수 있다.
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j-1][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1]);  neighborhood.add(image_pixel[i-1][j-1][1]);
            numberofneighborhood=6
    
    else: #그 외 행과 열이 모두 첫번째와 마지막이 아닌 경우에는 9개의 데이터를 저장하고, 열이 첫번째와 마지막인 경우에는 6개의 데이터만 저장한다.
        if(j==0): #마찬가지로 첫 번째 열과 마지막 열에서 index 침범이 발생하기 때문에 다른 방식으로 데이터를 저장한다.
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
            numberofneighborhood=6
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j-1][1])
            neighborhood.add(image_pixel[i][j][1]);  neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j-1][1]);
            numberofneighborhood=6
        else: #첫번째와 마지막 열을 제외한 나머지에서는 상하좌우 모든 방향으로 픽셀을 참조하고 이를 저장할 수 있다.
            neighborhood.add(image_pixel[i-1][j-1][1]); neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            neighborhood.add(image_pixel[i][j-1][1]); neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]);  
            neighborhood.add(image_pixel[i+1][j-1][1]); neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
    return ((len(neighborhood)/numberofneighborhood)<threshold)

def get_edges_neighborhood(image_pixel, threshold=0.5):
    #기존 get_edges와 동일한 방법으로 edges 여부를 결정하지만, 추가적으로 각 픽셀의 주변 픽셀들의 그룹도 고려한다. 만약 주변 픽셀들의 그룹이 서로 다르면 이를 노이즈라고 인식해서 edges로 분류하지 않는다.
    #이는 기존 gradient 방식에서 특정 픽셀 주변의 orientation을 보고, 그 값들이 서로 다른 경우 노이즈로 판단한 것과 동일한 맥락을 가진다. 이를 통햬 임계치를 낮춰서 디테일을 확보한 동시에 노이즈를 버릴 수 있다.
    #또는 특정 픽셀의 주변이 서로 다른 그룹으로 분류되고 있으면, 해당 픽셀이 안장점(saddle point)라고 할 수 있다. 왜냐하면 RGB공간에서 특정 픽셀의 주변이 서로 다른 그룹을 가진다는 것은 그 픽셀이 smooth하지 않다는 것을 말하기 때문이다.
    #input parameter 총 2개로 image_pixel은 픽셀에 대한 정보를 리스트 형식으로 저장하고 있는데, 여기서 정보는 해당 픽셀에서의 RGB정보와 픽셀이 분류되는 그룹 index에 대한 리스트를 말한다.
    #다른 input parameter인 threshold는 해당 픽셀의 이웃들을 확인하고 갯수대비 그룹의 수가 threshold보다 크면 noise로 판단하기 위해 사용된다.
    #출력 파라미터는 각 픽셀이 edges인가에 대한 정보를 담고 있는 리스트다. 해당 픽셀이 edges면 255 그렇지 않으면 0을 각 픽셀이 가지고 있다. 0과 1로 값을 넣어도 되지만 결과물을 편하게 출력하기 위해 0과 255로 edges 여부를 표기한다.
    #해당 픽셀과 양옆의 픽셀 또는 위아래의 픽셀과의 그룹을 비교하고, 두 가지 경우 중 최소 하나에 대해 다른 그룹이 존재한다고 판단되면 해당 픽셀을 edges라고 판단할 것이다.
    #이전 pre_processing에서 픽셀들을 이미 그룹으로 분류했기 때문에 사용할 수 있으며, 기존 방식과 달리 덧셈과 곱셈 연산을 수행하지 않아 속도가 빠를 수 있다.
    
    result=[] #각 픽셀의 edges인가를 0(edges가 아니다)와 255(edges가 맞다)으로 각 픽셀마다 저장하는 리스트이며, 이를 반환할 예정이다. 리스트는 기본적으로 shallow copy이기 때문에, 메모리 침범을 방지하고자 따로 리스트를 만들고자 한다.
    row_index_forgenerating=list(range(0, len(image_pixel), 1)) #result를 생성하기 위한 index 
    column_index=list(range(0, len(image_pixel[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(1, len(image_pixel)-1, 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다. 첫번째와 마지막 행은 따로 처리하기 때문에 이들은 제외한다.
    
    for i in row_index_forgenerating: #image_pixel은 각 픽셀의 밝기값과 픽셀이 속한 그룹을 가지고 있기 때문에, edges만을 저장하도록 데이터 구조를 정의한다. 
        result.append([])
        for j in column_index:
            result[i].append(0)
    del row_index_forgenerating #더 이상 필요없기 때문에 메모리를 절약하기 위해 삭제한다.
    
    for i in column_index:
        try:
            if(check_noise_neighborhood(image_pixel, 0, i, threshold)): #첫번째 열에 있는 픽셀 중 노이즈라고 판정된 픽셀에 대해서는 edges라고 하지 않는다.
                if((image_pixel[0][i][1]!=image_pixel[0][i+1][1]) or (image_pixel[0][i-1][1]!=image_pixel[0][i][1])): #아래 if-elif(else if)문은 첫번째 행에 있는 픽셀에 대해서 비교를 수행한다.                  
                    result[0][i]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                     result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            else:
                result[0][i]=0
            
            if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                #아래 if-elif(else if)문은 마지막 행에 있는 픽셀에 대해서 비교를 수행한다. 파이썬에서는 index가 음수면 마지막에 있는 객체부터 참조한다.
                test_group=(image_pixel[-1][i][1]!=image_pixel[-1][i+1][1]) or (image_pixel[-1][i-1][1]!=image_pixel[-1][i][1])
                if(test_group):
                     result[-1][i]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                     result[-1][i]=255
            else:
                 result[-1][i]=0
                    
        except: #첫번째 열과 마지막열에서는 index를 넘어가는 오류가 있기 때문에 이에 대해서도 별도의 방법으로 픽셀비교를 수행한다.
            if(i==0): #첫번째 열에 대해서는 오른쪽에 있는 픽셀만을 비교할 수 있다.
                if(check_noise_neighborhood(image_pixel, 0, i, threshold)):
                    if((image_pixel[0][i][1]!=image_pixel[0][i+1][1])):
                        result[0][i]=255 #특정픽셀과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                        result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                else:
                    result[0][i]=255 
                
                if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                    if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1])):
                        result[-1][i]=255 #특정픽셀과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif(column_index[-1][i][1]!=column_index[-2][i][1]):
                        result[-1][i]=255
                    
            else: #첫번째 열 외 오류가 날 수 있는 열은 마지막 열이며, 여기서는 왼쪽에 있는 픽셀만을 비교할 수 있다.
                if(check_noise_neighborhood(image_pixel, 0, i, threshold)):
                    if((image_pixel[0][i][1]!=image_pixel[0][i-1][1])):
                        result[0][i]=255 #특정픽셀과 왼쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                        result[0][i]=255 #특정픽셀과 아래쪽 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                else:
                     result[0][i]=0
                
                if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                    if((image_pixel[-1][i][1]!=image_pixel[-1][i-1][1])):
                        result[-1][i]=255 #특정픽셀과 왼쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                        result[-1][i]=255
                else:
                    result[-1][i]=0
    
    for i in row_index: #위의 반복문에서는 첫번째와 마지막 행에 대해 수행했기 때문에, 여기서는 나머지 행에 대해 edges 여부를 확인하고, edges면 255를 할당한다.
        for j in column_index:
            if(check_noise_neighborhood(image_pixel, i,j, threshold)): #좌표 (i,j)에 있는 픽셀의 주변을 확인하고, 이웃의 갯수대비 그룹의 비율이 threshold보다 크면 노이즈라고 판단해서 edges로 분류하지 않는다.
                try: 
                    if((image_pixel[i][j][1]!=image_pixel[i][j+1][1]) or (image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                        result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                         result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            
                except: #첫번째 열과 마지막열에서는 index를 넘어가는 오류가 있기 때문에 이에 대해서도 별도의 방법으로 픽셀비교를 수행한다.
                    if(i==0): #첫번째 열에 대해서는 오른쪽에 있는 픽셀만을 비교할 수 있다.
                        if((image_pixel[i][j][1]!=image_pixel[i][j+1][1])):
                            result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                        elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                             result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                    
                    else: #첫번째 열 외 오류가 날 수 있는 열은 마지막 열이며, 여기서는 왼쪽에 있는 픽셀만을 비교할 수 있다.
                        if((image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                            result[i][j]=255 #특정픽셀과 왼쪽과 오른쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
                        elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                            result[i][j]=255 #특정픽셀과 아래쪽과 위쪽의 픽셀의 그룹을 비교해서 다르면 해당 픽셀을 edges로 분류한다.
            else:
                result[i][j]=0
    
    return result

def changeforimage(Image):
    #입력파라미터는 전처리한 결과(pre_processing, pre_processing_total, pre_processing_color) 또는 각 픽셀의 edges이다.
    #출력파라마터는 전처리 결과에 맞는 이미지이다.
    #전처리 결과들이 서로 다른 값들을 반환하기 때문에 그에 맞도록 사진을 출력할 수 있는 데이터 구조를 반환해야 한다.
    
    from copy import deepcopy #파이썬에서는 리스트를 shallowcopy하기 때문에 이로 인한 문제를 방지하고자 deepcopy를 수행하는 라이브러리 및 함수이다. #내장 라이브러리다.
    result_pre_save1=deepcopy(Image) #사진으로 출력하기 위해 데이터 형식을 변환한다.
    column_index=list(range(0, len(Image[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
    row_index=list(range(0, len(Image), 1)) #이미지의 행을 참조할 수 있는 index를 저장한 리스트다.
    
    try:
        if(type(Image[0][0][0])==int): #입력파라미터가 밝기값과 그룹 인덱스를 각 픽셀마다 저장한 2D 리스트이다.
            try: #전처리 결과는 한 픽셀의 RGB정보 뿐만 아니라 그룹 index도 포함하고 있기 때문에, 전처리 결과를 춣력할 때만 이 반복문을 사용한다.
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0]
                return result_pre_save1
            except: #다만 edges는 그룹 index를 포함하지 않기 때문에 try 내의 반복문을 수행하면 오류가 발생한다. 그리고 edges는 각 픽셀의 밝기값만 저장하기 때문에 그대로 출력해도 무방하다.
                return result_pre_save1
        elif(len(Image[0][0][0])==3): #입력파라미터가 RGB값과 그룹 인덱스를 각 픽셀마다 저장한 2D 리스트이다.
            try: #전처리 결과는 한 픽셀의 RGB정보 뿐만 아니라 그룹 index도 포함하고 있기 때문에, 전처리 결과를 춣력할 때만 이 반복문을 사용한다.
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0]
                return result_pre_save1
            except:
                return result_pre_save1
        else: #pre_processing_total은 4차원 공간이기 때문에 이를 RGB 공간으로 사영(projection)시켜야 한다.
            try: 
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0][:3]
                return result_pre_save1
            except:
                return result_pre_save1
    except: #Image가 edges이기 때문에 값을 그대로 출력한다.
        return  result_pre_save1

##########################################################################################################################################
#여기서부터는 위의 코드를 실제로 활용하는 코드이기 떄문에, 결과를 재현하지 않을 예정이면 읽지 않아도 된다.
#아래 코드를 사용하기 위해서는 python3 -m pip install numpy, pandas, matplotlib, opencv-python를 terminal에서 수행해야 한다.

import cv2 #이미지 파일에 대한 읽기, 쓰기, 저장을 하기 위한 openCV 라이브러리다. #외부 라이브러리
from os import chdir #읽을 파일에 대한 대상을 지정하는 함수다. #내장 라이브러리 및 함수

#이미지가 저장된 경로를 설정한다. 사용자의 필요에 맞게 변형해야 한다.
chdir("//home//kimjungwoon//Desktop//3학년_2학기//컴퓨터비젼//테스트 파일") #리눅스OS의 종류인 루분투를 사용

#이미지의 종류는 총 2가지로 'test_ex2.jpg'와 'test_ex3.jpg'가 있다. 그리고 test_ex3로 edges를 얻는 경우 연산량이 많기 때문에 'test_ex2.jpg'로 코드 실행여부를 확인하는 것을 권장한다.
test_image=cv2.imread('test_ex2.jpg') #이미지 파일을 읽어온다. 흑백으로 읽기 위해서는 cv2.IMREAD_GRAYSCALE옵션을 input parameter로 추가한다.
test_image=list(test_image) #cv2가 array로 저장되기 때문에 데이터 변환이 용이한 리스트로 변환한다. #기본적으로 제공하는 자료구조다.
test_image_len=len(test_image) #이미지의 행의 갯수를 저장한다. #기본적으로 제공하는 함수다.

for i in range(0, test_image_len, 1): #원소들이 array형식으로 저장되어 있는데 데이터 변환의 편리함을 이유로 리스트로 바꾸고자 한다.
    test_image[i]=list(test_image[i])
    for j in range(0,len(test_image[0]), 1):
        test_image[i][j]=list(test_image[i][j])

column_index=list(range(0, len(test_image[0]),1)) #이미지의 열을 참조할 수 있는 index를 저장한 리스트다.
row_index=list(range(0, len(test_image), 1))

#위의 함수들을 실제로 사용하고 결과를 가져오기 위해서는 #(주석)을 제거하면 된다.

#아래 6줄은 test_ex.jpg에 대한 전처리 및 edges 구하는 것을 밝기값으로 수행한다.
#result_threshold=determine_distance(test_image) #threshold를 통계적으로 가져온다.
#result_pre_1=pre_processing(test_image, result_threshold[0]); #불러온 이미지를 밝기값에 대해 전처리를 수행하고 있다.
#result_pre2_1=pre_processing(test_image, result_threshold[1])
#result_pre3_1=pre_processing(test_image, result_threshold[2])
#result_edges_1=get_edges(result_pre_1) #전처리한 이미지에서 edges를 얻고자 한다.
#result_edges2_1=get_edges(result_pre2_1)
#result_edges3_1=get_edges(result_pre3_1)

#아래 3줄은 test_ex.jpg에 대한 edges 구하는 것을 밝기값으로 수행하지만, edges를 결정할 때 노이즈 여부를 추가적으로 판단한다.
#result_edges_1_noise=get_edges_neighborhood(result_pre_1, 0.4) #전처리한 이미지에서 edges를 얻고자 한다.
#result_edges2_1_noise=get_edges_neighborhood(result_pre2_1, 0.4)
#result_edges3_1_noise=get_edges_neighborhood(result_pre3_1, 0.4)

#아래 4줄은 test_ex.jpg에 대한 전처리 및 edges 구하는 것을 밝기값과 color정보로 수행한다.
result_pre1_total=pre_processing_total(test_image, 0.9)
result_edges1_total=get_edges(result_pre1_total)
result_pre2_total=pre_processing_total(test_image, 0.95)
result_edges2_total=get_edges(result_pre2_total)

#아래 2줄은 test_ex.jpg에 대한 edges 구하는 것을 밝기값과 color정보로 수행하지만, edges를 결정할 때 노이즈 여부를 추가적으로 판단한다.
result_edges1_total_noise=get_edges_neighborhood(result_pre1_total, 0.4)
result_edges2_total_noise=get_edges_neighborhood(result_pre2_total, 0.4)

#아래 6줄은 test_ex.jpg에 대한 전처리 및 edges 구하는 것을 color정보로 수행한다.
#result_pre1_color=pre_processing_color(test_image, 0.8)
#result_pre2_color=pre_processing_color(test_image, 0.95)
#result_pre3_color=pre_processing_color(test_image, 0.99)
#result_edges_color=get_edges(result_pre1_color)
#result_edges2_color=get_edges(result_pre2_color)
#result_edges3_color=get_edges(result_pre3_color)

#아래 3줄은 test_ex.jpg에 대한 edges 구하는 것을 color정보로 수행하지만, edges를 결정할 때 노이즈 여부를 추가적으로 판단한다.
#result_edges_color_noise=get_edges_neighborhood(result_pre1_color, 0.4)
#result_edges2_color_noise=get_edges_neighborhood(result_pre2_color, 0.4)
#result_edges3_color_noise=get_edges_neighborhood(result_pre3_color, 0.4)

result_pre_save1=changeforimage(result_pre1_total)
import matplotlib.pyplot as plt; plt.imshow(result_pre_save1); #사진을 출력하는데, parameter cmap='gray'는 흑백으로 사진을 출력한다.
plt.savefig('샘플2_컬러와 밝기_전처리_09.jpg',dpi=300) #출력한 사진을 저장한다.

result_pre_save2=changeforimage(result_edges1_total)
plt.imshow(result_pre_save2, cmap='gray'); #사진을 출력하는데, parameter cmap='gray'는 흑백으로 사진을 출력한다.
plt.savefig('샘플2_컬러와 밝기_edges_09.jpg', dpi=300) #출력한 사진을 저장한다.
