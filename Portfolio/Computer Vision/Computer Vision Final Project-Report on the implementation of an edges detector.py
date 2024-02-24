def pre_processing(image_pixel, distance=4):
    # This function categorizes pixels with similar brightness values into a group and modifies the brightness value of one object in the group with the brightness value of the other pixels.
    #There are two input parameters: image_pixel stores the brightness value of each pixel in the image, and distance is the distance between two pixels.
    #If the input parameter is not a 2D array of brightness values for each pixel, but RGB information is stored for each pixel, then the average of each RGB component of the pixel is taken.
    #The output parameter is a list of brightness values for each pixel and information about the group the pixel belongs to. The brightness value is the brightness of one object in the group to which the particular pixel is categorized.
    In the #Output parameter, it is possible to classify edges as edges by storing only the group index without storing the brightness value of each pixel. So if you want to use only the group index without utilizing the pixel information, you can modify image_pixel[i][j][1] of get_edges to image_pixel[i][j] to reduce the computation cost.
    #This is a smoothing operation like box-filter and Gaussian filter, but unlike those two methods, it doesn't reproduce a specific model, so it has more flexibility than before.
    #This can reduce the deviations caused by box and Gaussian filters. And this preprocessing assumes that the RGB and brightness values of a pixel are random variables, but they do not differ significantly under the same conditions.    
    
    result=[] #The result of the data change, and since Python makes shallow copies of lists, we save the result separately to avoid memory footprint.
    column_index=list(range(0, len(image_pixel[0]),1)) #A list of indexes to refer to the columns of the image.
    row_index=list(range(0, len(image_pixel), 1)) #A list that stores the index to reference the rows of the image. We'll use it in the for statement to avoid unnecessary iterations.
    
    for i in row_index: #We want to create the same number of pixels as the input parameter.
        result.append([])
        for j in column_index:
            result[i].append([])

    
    for i in row_index: #To be able to determine which group each pixel in image_pixel belongs to, we set up a data structure for it.
        for j in column_index: #Each pixel is stored with a very small memory allocation, so we store the value as an integer type to avoid overflow.
            try: #When we have stored the brightness value of each pixel, we execute the try statement, and when we have processed the RGB information of each pixel, we use the except statement to average the RGB and store it.
                temp=int(image_pixel[i][j]) #Python's lists can cause data leakage if used incorrectly, so we assign values to variables to prevent this.
            exception: #opencv has small memory for integers, so to avoid overflow, we convert to an integer type and perform the operation.
                temp=int(int(image_pixel[i][j][0])+int(image_pixel[i][j][1])+int(image_pixel[i][j][2]))/3
            result[i][j]=[temp, -1] #-1 means that the pixel is not classified.
    
    temp=result[0][0][0][0]
    result[0][0]=[temp, 0] #(0,0) defines that pixel belongs to the 0th group.
    
    group=[int(result[0][0][0][0])] #We're going to perform a task to categorize similar things based on a specific pixel. The set of pixels with similar brightness to pixel at coordinate (0,0) is the 0th group.
    for i in row_index: #Group pixels with similar brightness values together. i means row i occurrence (i is an integer).
        for j in column_index: #j is the jth column (j is an integer).
            group_index=0 #index of the group the pixel will be categorized into
            group_len=len(group) #number of groups
            min_distance_pixel_group=abs(result[i][j][0]-group[0])#To categorize certain pixels into groups, we first need to determine the initial value.
            
            for l in range(0, group_len, 1): #Find the group with the smallest difference in brightness values between pixels and groups, and iterate.
                if (abs(group[l]-result[i][j][0])<min_distance_pixel_group): 
                    min_distance_pixel_group=abs(group[l]-result[i][j][0])
                    group_index=l
                    
            if(abs(group[group_index]-result[i][j][0])<distance): #If the brightness difference between a pixel and a group is less than the threshold distance, classify the pixel into that group.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #If the brightness difference between the pixel and the group is less than the threshold distance, classify the pixel into that group.
                group.append(result[i][j][0]) #Add a new group.
                result[i][j][1]=len(group) #Taking len as index means taking the index of the newly added group.
    return result

def determine_distance(image_pixel):
    #input parameter image_pixel stores the brightness value of each pixel in the image.
    #This function averages the brightness values of the image and subtracts them from the brightness value of each pixel. Then, by listing the brightness values, we can get an ordinal statistic: find the two values (p-values) whose distance from the mean is statistically significant at 0.95.
    #We'll call these two values distance, which acts like a threshold in the canny edges vector.
    #This function can be used to statistically determine the distnace in pre_processing.
    #The output parameter is the median of the two distances and the mean minus the brightness value. The median is returned for those who want to use three thresholds later.
        
    distribution=[] #A list of all the brightness values for each pixel, which we want to average and then subtract the average for each element to estimate the distribution.
    column_index=list(range(0, len(image_pixel[0]),1)) #A list of indexes to reference the columns of the image.
    row_index=list(range(0, len(image_pixel), 1)) #A list of indexes to reference the rows of the image.
    
    for i in row_index: #The pixel is stored with a very small memory allocation, so we store the value as an integer to avoid overflow.
        for j in column_index:
            try: #We are processing based on a black and white image, so if we take a color image as a parameter, we will get an error.
                temp=int(image_pixel[i][j]) #We use temporary variables to avoid memory leaks caused by referencing lists.
                distribution.append(temp)
            except:
                temp=(int(image_pixel[i][j][0])+int(image_pixel[i][j][1])+int(image_pixel[i][j][2]))/3
                distribution.append(temp)
            
    distribution_size=len(distribution); distribution_mean=sum(distribution)/distribution_size #Get the average brightness of the images.
    for i in range(0,distribution_size,1): #Subtract the mean from the objects in the distribution.
        temp=abs(distribution[i]-distribution_mean) #Since we are looking at a distribution over a distance, we need to take the absolute value.
        distribution[i]=temp
    
    distribution.sort() #Sort the results in ascending order. This makes it easy to find the values that have a 0.05 and 0.95 probability of being away from the mean.
    stastic_095=0; stastic_005=0 #stastic_095 is the p-value that is greater than the median with a probability of 0.05 or less. stastic_005 is a p-value that has a probability of less than 0.05 of being less than the median.
    
    for i in range(0,distribution_size,1): #Find the index that has a 0.05 probability of falling away from the mean and get the corresponding value.
        if((i/distribution_size<=0.05) and (((i+1)/distribution_size>0.05)))): #The fact that the probability is less than 0.05 at time i but greater than 0.05 at time i+1 means that the cumulative distribution function is continuous, so there must be an index satisfying 0.05 between time i and time i+1 due to the median rule. However, since we are dealing with discrete data, we will take the i-th value as an approximation.
            stastic_005=abs(distribution[i]) #But since we're dealing with discrete data, we'll take the i-th value as an approximation.We also need to take the absolute value since we're looking for a distance.
            break #Break because we don't need to do any more iterations.
            
    for i in range(distribution_size-1, -1, -1): #Find the index that has a 0.95 probability of falling away from the mean and get the corresponding value.
        if((i/distribution_size>=0.95) and (((i-1)/distribution_size<0.95)))): #The fact that the probability is greater than 0.95 at time i but less than 0.95 at time i-1 means that the cumulative distribution function is continuous, so there must be an index between time i and time i+1 that satisfies 0.95 due to the midpoint theorem. However, since we are dealing with discrete data, we will take the i-th value as an approximation.
            stastic_095=abs(distribution[i]) #Since we're looking for a distance, we need to take the absolute value.
            break #Break because we don't need to do any more iterations.
    
    median=abs(distribution[int(distribution_size/2)]) #Get the median.
    return [stastic_005, median, stastic_095]

def pre_processing_color(image_pixel, correlation=0.8):
    # 2 input parameters image_pixel stores the RGB value of each pixel in the image, and correlation is the similarity to classify two vectors into the same group in RGB space.
    In #pre_processing, pixels were categorized into the same group if the difference between their brightness values is less than a certain threshold. Here, we find the inner product of the vector between a specific pixel and the representative value of the group in RGB space, and if the value is greater than correlation, we categorize them into the same group.
    #The output parameter is a list of RGB values for each pixel and information about the group it belongs to.
    #The problem with pre_processing is that it doesn't perform well in situations where the brightness values are similar, so we use the color information directly.
    #This preprocessing assumes that the RGB of the pixels are not significantly different under the same conditions.    
    
    result=[] #The result of the data changes, and since Python makes shallow copies of lists, we store the result separately to avoid memory footprint.
    column_index=list(range(0, len(image_pixel[0]),1)) #A list of indexes to refer to the columns of the image.
    row_index=list(range(0, len(image_pixel), 1)) #A list that stores the index to reference the rows of the image. We'll use it in the for statement to avoid unnecessary iterations.
    
    for i in row_index: #We want to make the number of pixels equal to the input parameter.
        result.append([])
        for j in column_index:
            result[i].append([])
    
    for i in row_index: #To be able to determine which group each pixel in image_pixel belongs to, we set up a data structure accordingly.
        for j in column_index:
            #opencv stores RGB values as integers, which are very small in memory. This can cause an overflow when computing large values, so to avoid this, we use a large memory int.
            temp=[int(image_pixel[i][j][0]),int(image_pixel[i][j][1]), int(image_pixel[i][j][2])] #Python's lists can cause data leaks if used incorrectly, so we assign values to variables to prevent this.
            result[i][j]=[temp, -1] #-1 means that the pixel is not classified.
    
    temp=result[0][0][0][0]
    result[0][0]=[temp, 0] #(0,0) defines that pixel belongs to the 0th group.
    
    group=[result[0][0][0][0]] #We're going to do the task of categorizing similar things based on a specific pixel. The set of pixels with coordinates (0,0) and their respective RGBs is the 0th group.
    for i in row_index: #Find the inner product between each pixel and the representative object of the group in RGB space, and if the result is above a threshold, classify them as the same group, otherwise declare the pixel as the representative object of a new group.
        for j in column_index: #i means the i-th row (i is an integer). j means jth column (j is an integer).
            group_index=0 #group index to categorize the pixel into
            group_len=len(group) #number of groups
            
            #The following 3 lines find the inner product in RGB space between the representative object of the 0th group and the corresponding (i,j) object. This serves as an initial value for comparison with other groups.
            group_object_size=(group[0][0]**2+group[0][1]**2+group[0][2]**2)**(0.5) #Euclidean size of the representative of the 0th group
            pixel_size=(result[i][j][0][0]**2+result[i][j][0][1]**2+result[i][j][0][2]**2)**(0.5) #pixel의 유클리드 크기
            product=(group[0][0]*result[i][j][0][0])+(group[0][1]*result[i][j][0][1])+(group[0][2]*result[i][j][0][2])#0번째 group의 대표값과 pixel간의 내적
            
            try:
                max_correlation=(product)/(group_object_size*pixel_size) #In order to classify a particular pixel into a group, we must first determine its initial value.
            except:
                #if max_correlation=0 #pixel_size is 0, an error has occurred, which means that the pixel is at the origin, so it is safe to assign it to 0.
            
            #If the similarity of two vectors in RGB space is greater than the threshold correlation, they will be categorized into the same group. In RGB space, all values are positive, so there are no negative internals.
            for l in range(0, group_len, 1): #This iteration finds the group with the highest correlation between pixels and groups.
                try:
                    #Iterate to find the group with the largest correlation. group_object_size=(group[l][0]**2+group[l][1]**2+group[l][2]**2)**(0.5) #Euclidean size of the representative of the lth group.
                    product=(group[l][0]*result[i][j][0][0])+(group[l][1]*result[i][j][0][1])+(group[l][2]*result[i][j][0][2])#0번째 group의 대표값과 pixel간의 내적
                    compare_correlation=product/(group_object_size*pixel_size)#internal between representative value of lth group and pixel (i,j)
                except:
                    compare_correlation=0 #Here again, if pixel_size is 0, an error has occurred, which means that the pixel is at the origin, so it is safe to assign it as 0.
                
                if (compare_correlation>max_correlation): #We are looking for the group with the highest similarity to a particular pixel.
                    max_correlation=compare_correlation
                    group_index=l
            
            if(max_correlation>correlation): #If the correlation between a pixel and a group is higher than the threshold, classify the pixel as a group.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #If the brightness difference between the pixel and the group is less than the threshold distance, classify the pixel into that group.
                group.append(result[i][j][0]) #Add a new group.
                result[i][j][1]=len(group) #Taking len as index means taking the index of the newly added group.
    return result

def pre_processing_total(image_pixel, correlation=0.8):
    # 2 input parameters image_pixel stores the RGB value of each pixel in the image, and correlation is a criterion that allows two vectors to be categorized into the same group in RGBL (RGB+brightness) space.
    The #pre_processing_color classifies pixels into a specific group based on RGB, where we add brightness value information to RGB to find the inner product of the vector between a specific pixel and a representative object of the group in a four-dimensional space, and if the value is greater than the correlation, it is classified into the same group.
    #The output parameter is a list of RGBL values for each pixel (L is the brightness value of the pixel) and information about the group to which the pixel belongs.
    Since #pre_processing_color only considers RGB, there may be situations where pixels are similar in color despite having different brightness values, and therefore cannot be classified as edges. To overcome this, this function uses both RGB and brightness information.
    #This preprocessing assumes that the RGBs of the pixels are not significantly different under the same conditions.    
    
    result=[] #The result of the data transformation is that we are storing four-dimensional data in RGBL instead of RGB, so we need to be careful when representing the image.
    column_index=list(range(0, len(image_pixel[0]),1)) #A list of indexes to refer to the columns of the image.
    row_index=list(range(0, len(image_pixel), 1)) #A list that stores the index to reference the rows of the image. We'll use it in the for statement to avoid unnecessary iterations.
    
    for i in row_index: #We want to create the same number of pixels as the input parameter.
        result.append([])
        for j in column_index:
            result[i].append([])
    
    for i in row_index: #To be able to determine which group each pixel in image_pixel belongs to, we set up a data structure for it.
        for j in column_index:
            #opencv stores RGB values as integers, which are very small in memory. This can cause an overflow when computing large values, so to avoid this, we use an int with large memory.
            temp=[int(image_pixel[i][j][0]),int(image_pixel[i][j][1]), int(image_pixel[i][j][2])] #Python's lists can cause data leaks if used incorrectly, so we assign values to variables to prevent this.
            temp.append(int(sum(temp)/3)) #We want to create a 4-dimensional space with brightness values appended to the existing RGB space.
            result[i][j]=[temp, -1] #-1 means that the pixel is unclassified.
    
    temp=result[0][0][0][0]
    result[0][0]=[temp, 0] #(0,0) defines that pixel belongs to the 0th group.
    
    group=[result[0][0][0][0]] #We're going to do the task of categorizing similar things based on a specific pixel. The set of pixels with coordinates (0,0) and similar RGBLs is the 0th group.
    for i in row_index:
        # for j in column_index: #j means the jth column (j is an integer).
            group_index=0 #index of the group the pixel will be categorized into
            group_len=len(group) #number of groups
            
            group_object_size=(group[0][0]**2+group[0][1]**2+group[0][2]**2+group[0][3]**2)**(0.5) #Euclidean size of the representative value of the 0th group
            pixel_size=(result[i][j][0][0]**2+result[i][j][0][1]**2+result[i][j][0][2]**2++result[i][j][0][3]**2)**(0.5) #pixel의 유클리드 크기
            product=(group[0][0]*result[i][j][0][0])+(group[0][1]*result[i][j][0][1])+(group[0][2]*result[i][j][0][2])+(group[0][3]*result[i][j][0][3])#0번째 group의 대표값과 pixel간의 내적
            
            try:
                max_correlation=(product)/(group_object_size*pixel_size) #In order to classify a particular pixel into a group, we must first determine its initial value.
            except:
                #if max_correlation=0 #pixel_size is 0, an error has occurred, which means that the pixel is at the origin, so it is safe to assign it to 0.
            
            #In RGB space, two vectors will be categorized into groups if their similarity is greater than a threshold correlation. In RGBL space, all values are positive, so there are no negative inliers.
            for l in range(0, group_len, 1): #This iteration finds the group with the highest correlation between pixels and groups and the smallest difference in brightness values.               
                try:
                    #Iterate to find the group with the smallest difference in brightness values. group_object_size=(group[l][0]**2+group[l][1]**2+group[l][2]**2+group[l][3]**2)**(0.5) #Euclidean size of the representative value of the lth group.
                    product=(group[l][0]*result[i][j][0][0])+(group[l][1]*result[i][j][0][1])+(group[l][2]*result[i][j][0][2])+(group[l][3]*result[i][j][0][3])#0번째 group의 대표값과 pixel간의 내적
                    compare_correlation=product/(group_object_size*pixel_size)#internal between representative value of lth group and pixel (i,j)
                except:
                    compare_correlation=0 #Here again, if pixel_size is 0, an error has occurred, which means that the pixel is at the origin, so it is safe to assign it as 0.
                
                if (compare_correlation>max_correlation): #We are looking for the group with the highest similarity to a specific pixel.
                    max_correlation=compare_correlation
                    group_index=l
            
            if(max_correlation>correlation): #If the correlation between a pixel and a group is higher than the threshold, classify the pixel as a group.
                result[i][j][0]=group[group_index]
                result[i][j][1]=group_index
            else: #If the brightness difference between the pixel and the group is less than the threshold distance, classify the pixel into that group.
                group.append(result[i][j][0]) #Add a new group.
                result[i][j][1]=len(group) #Taking len as index means taking the index of the newly added group.
    return result

def get_edges(image_pixel):
    #input parameters image_pixel stores information about a pixel in the form of a list, where the information is a list of the RGB information at that pixel and the group index into which the pixel is categorized.
    #The output parameter is a list that contains information about whether each pixel is an edge. Each pixel has a value of 255 if it is an edge and 0 otherwise. The values could be 0 and 1, but we use 0 and 255 to indicate whether the pixel is an edge for ease of output.
    #We will compare the grouping of the pixel with its neighbors or with the pixels above and below it, and if we determine that a different grouping exists for at least one of the two cases, we will consider the pixel an edge.
    #This method can be used because we have already categorized the pixels into groups in the previous pre_processing, and can be faster because it does not perform addition and multiplication operations as the previous method does.
    
    result=[] # This is a list that stores for each pixel whether it is an edge or not, 0 (not an edge) and 255 (yes, it is an edge), and we will return it. Since the list is a shallow copy by default, we want to create a separate list to avoid memory encroachment.
    row_index_forgenerating=list(range(0, len(image_pixel), 1)) #index to generate result 
    column_index=list(range(0, len(image_pixel[0]),1)) #a list that stores the index to reference the column of the image.
    row_index=list(range(1, len(image_pixel)-1, 1)) #A list of indices to reference the rows of the image. We exclude the first and last rows because we'll handle them separately.
    
    for i in row_index_forgenerating: #image_pixel has the brightness value of each pixel and the group it belongs to, so we define a data structure to store only edges. 
        result.append([])
        for j in column_index:
            result[i].append(0)
    del row_index_forgenerating #Delete it to save memory since we don't need it anymore.
    
    for i in column_index: #The first and last rows cannot be compared to pixels in all directions, so we perform a pixel comparison for some directions.
        try: 
            #The if-elif(else if) statement below performs the comparison on the pixels in the first row.
            if((image_pixel[0][i][1]!=image_pixel[0][i+1][1]) or (image_pixel[0][i-1][1]!=image_pixel[0][i][1])):
                result[0][i]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
            elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                #compare a particular pixel with a group of pixels below it and classify it as an edge if it is different. result[0][i]=255 #compare a particular pixel with a group of pixels below it and classify it as an edge if.
            
            #The if-elif(else if) statement below performs the comparison on the pixels in the last row. In Python, if index is negative, the last object is referenced first.
            if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1]) or (image_pixel[-1][i-1][1]!=image_pixel[-1][i][1])):
                 result[-1][i]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
            elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                 result[-1][i]=255
                    
        exception: #In the first and last columns, there is an error of exceeding the index, so we perform the pixel comparison separately.
            if(i==0): #For the first column, we can only compare the pixels on the right.
                if((image_pixel[0][i][1]!=image_pixel[0][i+1][1])):
                    result[0][i]=255 #Compare a particular pixel with the group of pixels to its right, and if they are different, classify them as edges.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                    #compare a particular pixel with a group of pixels below it, and if they are different, classify them as edges.
                
                if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1])):
                    #compare a particular pixel with the group of pixels to its right and classify it as an edge if they are different.
                elif(column_index[-1][i][1]!=column_index[-2][i][1]):
                    #result[-1][i]=255
                    
            else: #The only column besides the first that can give an error is the last column, and here we can only compare the pixels on the left.
                if((image_pixel[0][i][1]!=image_pixel[0][i-1][1])):
                    #compare a particular pixel with the group of pixels to its left, and if they are different, classify them as edges.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                    #compare a particular pixel with a group of pixels below it, and if they are different, classify them as edges.
                
                if((image_pixel[-1][i][1]!=image_pixel[-1][i-1][1])):
                    result[-1][i]=255 #Compare a particular pixel with the group of pixels to its left and classify it as an edge if they are different.
                elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                    result[-1][i]=255
    
    for i in row_index: #In the above iteration, we did this for the first and last rows, so here we check for edges for the rest of the rows and assign 255 if there are edges.
        for j in column_index:
            try: 
                if((image_pixel[i][j][1]!=image_pixel[i][j+1][1]) or (image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                    result[i][j]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
                elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                     #compare a particular pixel with a group of pixels below and above it, and if they are different, classify them as edges.
            
            exception: #In the first and last columns, there is an error of exceeding the index, so we perform the pixel comparison separately.
                if(i==0): #For the first column, we can only compare pixels on the right.
                    if((image_pixel[i][j][1]!=image_pixel[i][j+1][1])):
                        #compare a particular pixel with the group of pixels to its left and right, and if they are different, classify them as edges.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                         #compare a particular pixel with the group of pixels below and above it and if they are different, classify them as edges.
                    
                else: #The only column besides the first that could be in error is the last column, where we can only compare pixels on the left.
                    if((image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                        #compare a particular pixel with the group of pixels to its left and right, and if they are different, classify them as edges.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                        #compare a particular pixel with a group of pixels below and above it, and if they are different, classify them as edges.
    
    return result

def check_noise_neighborhood(image_pixel,i,j, threshold):
    #Checks for r groups of neighborhoods of pixel (i,j), and if the ratio of group types and neighborhoods is greater than threshold (a real number between 0 and 1), the pixel is considered noise.
    #The input parameters are the coordinates (i,j) of the pixel, threshold and image_pixel, and the output parameter is bool (0 means that the (i,j) coordinates are noise).
    #This is used in get_edges_neighborhood, so the variable image_pixel used in that function is an input parameter to get_edges_neighborhood.
    
    neighborhood=set() #Sets, unlike lists, do not store elements in duplicate, so we know which groups are in the neighborhood of a particular pixel.
    numberofneighborhood=9 #Number of neighborhoods for a pixel, and since 3x3 references are the most common, you can save computation by setting the default to 9.
    if(i==0): #The first and last rows will only check 6 neighborhoods because checking 3x3 neighborhoods will result in an error due to index encroachment.
        if(j==0): #Similarly, the first and last columns will encounter index violations, so we store the data in a different way.
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
            numberofneighborhood=4 #We only know of 4 neighborhoods for this pixel, so we modify the value.
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j-1][1])
            numberofneighborhood=4
        else: #Except for the first and last columns, we can reference and store pixels in the left, right, and up and down directions (0th row only down, last row only up).
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]); neighborhood.add(image_pixel[i+1][j-1][1]); neighborhood.add(image_pixel[i+1][j-1][1]);
            numberofneighborhood=6
    
    elif(i==len(image_pixel)):
        #similarly, we store the data in a different way because the index encroachment occurs in the first and last columns.
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            numberofneighborhood=4
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j-1][1])
            numberofneighborhood=4
        else: #Except for the first and last columns, we can refer to and store pixels in the left, right, and up and down directions (0th row only down, last row only up).
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j-1][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1]); neighborhood.add(image_pixel[i-1][j-1][1]);
            numberofneighborhood=6
    
    else: #store 9 data if the row and column are not both first and last, and only 6 data if the column is first and last.
        if(j==0): #Similarly, we store the data in a different way because index encroachment occurs in the first and last columns.
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
            numberofneighborhood=6
        elif(j==(len(image_pixel[0])-1)):
            neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j-1][1])
            neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j-1][1]); 
            neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j-1][1]);
            numberofneighborhood=6
        else: #Except for the first and last columns, we can reference and store pixels in all directions, up, down, left, and right.
            neighborhood.add(image_pixel[i-1][j-1][1]); neighborhood.add(image_pixel[i-1][j][1]); neighborhood.add(image_pixel[i-1][j+1][1])
            neighborhood.add(image_pixel[i][j-1][1]); neighborhood.add(image_pixel[i][j][1]); neighborhood.add(image_pixel[i][j+1][1]);  
            neighborhood.add(image_pixel[i+1][j-1][1]); neighborhood.add(image_pixel[i+1][j][1]); neighborhood.add(image_pixel[i+1][j+1][1]); neighborhood.add(image_pixel[i+1][j+1][1]);
    return ((len(neighborhood)/numberofneighborhood)<threshold)

def get_edges_neighborhood(image_pixel, threshold=0.5):
    # Determines whether there is an edge in the same way as get_edges, but additionally considers the group of neighboring pixels for each pixel. If the neighboring pixels are different from each other, they are recognized as noise and not classified as edges.
    #This is in the same vein as the traditional gradient method, which looks at the orientation around a particular pixel and determines that if the values are different, it is noise. This allows us to lower the threshold to retain detail while discarding noise.
    #Alternatively, if the surroundings of a particular pixel are categorized into different groups, the pixel may be called a saddle point. This is because in RGB space, having different groups around a pixel indicates that the pixel is not smooth.
    #With two input parameters, image_pixel stores information about a pixel in the form of a list, where the information is a list of the RGB information at the pixel and the group index into which the pixel is categorized.
    #The other input parameter, threshold, is used to check the pixel's neighbors and determine if the number of groups is greater than the threshold.
    #The output parameter is a list that contains information about whether each pixel is an edge. Each pixel has a value of 255 if it is an edge and 0 otherwise. The values could be 0 and 1, but we use 0 and 255 to indicate whether the pixel is an edge for ease of output.
    #We will compare the grouping of the pixel with its neighbors or with the pixels above and below it, and if we determine that a different grouping exists for at least one of the two cases, we will consider the pixel an edge.
    #This method can be used because we have already categorized the pixels into groups in the previous pre_processing, and can be faster because it does not perform addition and multiplication operations, unlike the previous method.
    
    result=[] # This is a list that stores for each pixel whether it is an edge or not, 0 (not an edge) and 255 (yes, it is an edge), and we will return it. Since the list is a shallow copy by default, we want to create a separate list to avoid memory encroachment.
    row_index_forgenerating=list(range(0, len(image_pixel), 1)) #index to generate result 
    column_index=list(range(0, len(image_pixel[0]),1)) #a list that stores the index to reference the column of the image.
    row_index=list(range(1, len(image_pixel)-1, 1)) #A list of indices to reference the rows of the image. We exclude the first and last rows because we'll handle them separately.
    
    for i in row_index_forgenerating: #image_pixel has the brightness value of each pixel and the group it belongs to, so we define a data structure to store only edges. 
        result.append([])
        for j in column_index:
            result[i].append(0)
    del row_index_forgenerating #Delete it to save memory since we don't need it anymore.
    
    for i in column_index:
        try:
            #Don't call edges for pixels in the first column that are determined to be noise. if(check_noise_neighborhood(image_pixel, 0, i, threshold)): #Don't call edges for pixels in the first column that are determined to be noise.
                if((image_pixel[0][i][1]!=image_pixel[0][i+1][1]) or (image_pixel[0][i-1][1]!=image_pixel[0][i][1])): #The following if-elif(else if) statement performs a comparison on the pixels in the first row.                  
                    result[0][i]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
                elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                     #compare a particular pixel with a group of pixels below it, and if they are different, classify them as edges.
            else:
                result[0][i]=0
            
            if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                # The if-elif (else if) statement below performs the comparison on the pixels in the last row. In Python, if index is negative, the last object is referenced first.
                test_group=(image_pixel[-1][i][1]!=image_pixel[-1][i+1][1]) or (image_pixel[-1][i-1][1]!=image_pixel[-1][i][1])
                if(test_group):
                     result[-1][i]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
                elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                     result[-1][i]=255
            else:
                 result[-1][i]=0
                    
        exception: #In the first and last columns, there is an error of exceeding the index, so we perform the pixel comparison separately.
            if(i==0): #For the first column, we can only compare the pixels on the right.
                if(check_noise_neighborhood(image_pixel, 0, i, threshold)):
                    if((image_pixel[0][i][1]!=image_pixel[0][i+1][1])):
                        result[0][i]=255 #Compare a particular pixel with the group of pixels to its right, and if they are different, classify them as edges.
                    elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                        #compare a particular pixel with a group of pixels below it, and if they are different, classify them as edges.
                else:
                    result[0][i]=255 
                
                if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                    if((image_pixel[-1][i][1]!=image_pixel[-1][i+1][1])):
                        result[-1][i]=255 #Compare a particular pixel with the group of pixels to its right, and if they are different, classify them as edges.
                    elif(column_index[-1][i][1]!=column_index[-2][i][1]):
                        #result[-1][i]=255
                    
            else: #The only column besides the first one that can give an error is the last one, and here we can only compare the pixels on the left.
                if(check_noise_neighborhood(image_pixel, 0, i, threshold)):
                    if((image_pixel[0][i][1]!=image_pixel[0][i-1][1])):
                        result[0][i]=255 #Compare a particular pixel with the group of pixels to its left, and if they are different, classify them as edges.
                    elif(image_pixel[0][i][1]!=image_pixel[1][i][1]):
                        #compare a particular pixel with a group of pixels below it, and if they are different, classify them as edges.
                else:
                     result[0][i]=0
                
                if(check_noise_neighborhood(image_pixel, -1, i, threshold)):
                    if((image_pixel[-1][i][1]!=image_pixel[-1][i-1][1])):
                        result[-1][i]=255 #Compare a particular pixel with the group of pixels to its left, and if they are different, classify them as edges.
                    elif(image_pixel[-1][i][1]!=image_pixel[-2][i][1]):
                        result[-1][i]=255
                else:
                    result[-1][i]=0
    
    for i in row_index: #In the above iteration, we did this for the first and last rows, so here we check for edges for the rest of the rows and assign 255 if there are edges.
        for j in column_index:
            if(check_noise_neighborhood(image_pixel, i,j, threshold)): #Check the neighborhood of the pixel at coordinate (i,j), and if the ratio of the group to the number of neighbors is greater than threshold, it is noise and not classified as an edge.
                try: 
                    if((image_pixel[i][j][1]!=image_pixel[i][j+1][1]) or (image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                        result[i][j]=255 #Compare a particular pixel with a group of pixels to its left and right, and if they are different, classify them as edges.
                    elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                         #compare a particular pixel with a group of pixels below and above it, and if they are different, classify them as edges.
            
                exception: #In the first and last columns, there is an error of exceeding the index, so we perform the pixel comparison separately.
                    if(i==0): #For the first column, we can only compare pixels on the right.
                        if((image_pixel[i][j][1]!=image_pixel[i][j+1][1])):
                            #compare a particular pixel with the group of pixels to its left and right, and if they are different, classify them as edges.
                        elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                             #compare a particular pixel with the group of pixels below and above it and if they are different, classify them as edges.
                    
                    else: #The only column besides the first that could be in error is the last column, where we can only compare pixels on the left.
                        if((image_pixel[i][j][1]!=image_pixel[i][j-1][1])):
                            #compare a particular pixel with the group of pixels to its left and right, and if they are different, classify them as edges.
                        elif((image_pixel[i-1][j][1]!=image_pixel[i][j][1]) or (image_pixel[i+1][j][1]!=image_pixel[i][j][1])):
                            #compare a particular pixel with a group of pixels below and above it and if they are different, classify them as edges.
            else:
                result[i][j]=0
    
    return result

def changeforimage(Image):
    # input parameters are the preprocessing results (pre_processing, pre_processing_total, pre_processing_color) or the edges of each pixel.
    #The output parameter is the image that fits the preprocessing results.
    #Since different preprocessing results return different values, we need to return a data structure that can output a picture accordingly.
    
    from copy import deepcopy #Python shallowcopies lists, so this is a library and function that performs deepcopy to avoid this problem. # built-in library.
    result_pre_save1=deepcopy(Image) #Convert the data format to output as an image.
    column_index=list(range(0, len(Image[0]),1)) #A list of indexes to reference the columns of the image.
    row_index=list(range(0, len(Image), 1)) #A list of indexes to reference the rows of the image.
    
    try:
        if(type(Image[0][0][0][0])==int): #The input parameter is a 2D list that stores the brightness value and group index for each pixel.
            try: #The preprocessing result contains not only the RGB information of a pixel, but also the group index, so this iteration is only used to print the preprocessing result.
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0]
                return result_pre_save1
            Except: #But edges does not contain a group index, so iterating within try will result in an error, and edges only stores the brightness value of each pixel, so it's okay to print it as is.
                return result_pre_save1
        elif(len(Image[0][0][0][0])==3): #The input parameter is a 2D list of RGB values and group indices stored for each pixel.
            try: #The preprocessing result contains not only the RGB information of one pixel, but also the group index, so this iteration is only used to print the preprocessing result.
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0]
                return result_pre_save1
            except:
                return result_pre_save1
        else: #pre_processing_total is a 4-dimensional space, so we need to project it to RGB space.
            try: 
                for i in row_index:
                    for j in column_index:
                        result_pre_save1[i][j]=result_pre_save1[i][j][0][:3]
                return result_pre_save1
            except:
                #Image is editable. return result_pre_save1
    exception: #Output the value as it is because Image is an edge.
        return result_pre_save1

##########################################################################################################################################
#This is the code that actually utilizes the code above, so don't read it if you're not going to reproduce the results.
#To use the code below, run python3 -m pip install numpy, pandas, matplotlib, and opencv-python in the terminal.

import cv2 #The openCV library for reading, writing, and saving image files. #External libraries
from os import chdir #Function to specify the destination for the file to be read. #Internal libraries and functions

#Set the path where the image is stored. You should modify this to suit your needs.
chdir("//home//kimjungwoon//Desktop//3학년_2학기//ComputerVision//TestFile") #Uses Ubuntu, a type of Linux OS.

#There are two types of images, 'test_ex2.jpg' and 'test_ex3.jpg'. And if you get edges with test_ex3, it is recommended to check the code execution with 'test_ex2.jpg' because it is computationally expensive.
test_image=cv2.imread('test_ex2.jpg') #Read the image file. Add the cv2.IMREAD_GRAYSCALE option as an input parameter to read in grayscale.
test_image=list(test_image) #Convert cv2 to a list for easy data conversion since it is stored as an array. #This is the built-in data structure.
test_image_len=len(test_image) #Stores the number of rows in the image. #This is a built-in function.

for i in range(0, test_image_len, 1): #The elements are stored as an array, but we want to convert them to a list for the convenience of data conversion.
    test_image[i]=list(test_image[i])
    for j in range(0,len(test_image[0]), 1):
        test_image[i][j]=list(test_image[i][j])

column_index=list(range(0, len(test_image[0]),1)) #A list that stores the index to refer to the column of the image.
row_index=list(range(0, len(test_image), 1))

#To actually use the above functions and get the results, we can remove the #(comments).

#The following 6 lines perform preprocessing and edges finding for test_ex.jpg with brightness values.
#result_threshold=determine_distance(test_image) #get the threshold statistically.
#result_pre_1=pre_processing(test_image, result_threshold[0]); #Pre-process the imported image for brightness values.
#result_pre2_1=pre_processing(test_image, result_threshold[1])
#result_pre3_1=pre_processing(test_image, result_threshold[2])
#result_edges_1=get_edges(result_pre_1) #Get the edges from the preprocessed image.
#result_edges2_1=get_edges(result_pre2_1)
#result_edges3_1=get_edges(result_pre3_1)

#The following 3 lines do the same thing as getting edges for test_ex.jpg with brightness values, but additionally determine if there is noise when determining edges.
#result_edges_1_noise=get_edges_neighborhood(result_pre_1, 0.4) #We want to get the edges from the preprocessed image.
#result_edges2_1_noise=get_edges_neighborhood(result_pre2_1, 0.4)
#result_edges3_1_noise=get_edges_neighborhood(result_pre3_1, 0.4)

#The following 4 lines perform preprocessing and edges retrieval for test_ex.jpg with brightness values and color information.
result_pre1_total=pre_processing_total(test_image, 0.9)
result_edges1_total=get_edges(result_pre1_total)
result_pre2_total=pre_processing_total(test_image, 0.95)
result_edges2_total=get_edges(result_pre2_total)

#The following two lines do the same thing as getting edges for test_ex.jpg with the brightness value and color information, but additionally check for noise when determining edges.
result_edges1_total_noise=get_edges_neighborhood(result_pre1_total, 0.4)
result_edges2_total_noise=get_edges_neighborhood(result_pre2_total, 0.4)

#The following 6 lines perform preprocessing and getting edges for test_ex.jpg with color information.
#result_pre1_color=pre_processing_color(test_image, 0.8)
#result_pre2_color=pre_processing_color(test_image, 0.95)
#result_pre3_color=pre_processing_color(test_image, 0.99)
#result_edges_color=get_edges(result_pre1_color)
#result_edges2_color=get_edges(result_pre2_color)
#result_edges3_color=get_edges(result_pre3_color)

#The following 3 lines do the same thing as getting edges for test_ex.jpg with color information, but additionally check for noise when determining edges.
#result_edges_color_noise=get_edges_neighborhood(result_pre1_color, 0.4)
#result_edges2_color_noise=get_edges_neighborhood(result_pre2_color, 0.4)
#result_edges3_color_noise=get_edges_neighborhood(result_pre3_color, 0.4)

result_pre_save1=changeforimage(result_pre1_total)
import matplotlib.pyplot as plt; plt.imshow(result_pre_save1); #Display the picture, parameter cmap='gray' will display the picture in black and white.
plt.savefig('sample2_color and brightness_preprocess_09.jpg',dpi=300) #Save the output photo.

result_pre_save2=changeforimage(result_edges1_total)
plt.imshow(result_pre_save2, cmap='gray'); #Display the image, where the parameter cmap='gray' displays the image in black and white.
plt.savefig('sample2_color and brightness_edges_09.jpg', dpi=300) #Save the output photo.