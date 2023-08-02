from django.db import models
from django.forms import ModelForm # 모델 폼 설정

from django.conf import settings

#회원 테이블
class Users(models.Model):
    user_name = models.CharField(max_length= 20 , unique=True)
    user_date = models.DateTimeField(auto_now_add=True) #가입일(처음 등록한 시간으로 저장)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length = 100)
    user_gender = models.IntegerField(default=0,blank=True, null=True)
    user_age = models.IntegerField(default=0, blank=True, null=True)
    def __str__(self):
        return f'{self.user_name}'
    class Meta:
        db_table = 'user_tb'

#거래글 테이블
class Item(models.Model):
    item_name = models.CharField(max_length = 20)
    user_name = models.ForeignKey(Users, to_field='user_name', related_name='seller', on_delete = models.CASCADE, db_column="user_name", max_length= 20, null=True) #fk추가
    STATUS = (('거래 전','거래 전'), ('거래 완료','거래 완료')) # 전자가 테이블 컬럼 출력값, 후자가 admin 페이지에서 출력
    trade_status = models.CharField(max_length=5, default='거래 전', choices=STATUS, null=True) #거래상태(판매중,거래완료)
    item_price = models.IntegerField(null=True)
    item_content = models.TextField(max_length = 200) 
    item_img = models.ImageField(upload_to="images/", blank=True, null=True)
    
    # item_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'[{self.pk}]{self.item_name}'

    def get_absolute_url(self):
        return f'/posting/{self.pk}/'
    
    class Meta:
        db_table = 'item_tb'

#댓글 테이블       
class Comment(models.Model):
    #pk(댓글번호)는 자동생성(id)
    user_name = models.ForeignKey(Users, to_field='user_name', related_name='commenter', on_delete = models.CASCADE,
                                  db_column="user_name", max_length= 20, null=True) #댓글/답글 작성자
    item_id = models.ForeignKey(Item, to_field='id', related_name='post', on_delete = models.CASCADE, db_column="item_id") #게시글ID
    comment = models.TextField() #댓글/답글 내용
    comment_date = models.DateTimeField(auto_now_add=True) #등록날짜
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply')

    class Meta:
        ordering=['-comment_date'] #댓글작성시간 내림차순

    def __str__(self):
        return str(self.user_name) + 'comment' + str(self.comment)

    @property
    def children(self): #답글일 경우
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None: #댓글일 경우
            return True
        return False

#데이터 분석용 거래완료 테이블    
class Trade(models.Model):
        item_img = models.ImageField(upload_to="trade_images/", blank=True, null=True)
        item_price = models.IntegerField(null=True)
        item_date = models.DateField(auto_now_add=True,null=True)