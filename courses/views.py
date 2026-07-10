from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from .models import Course, Category, Lesson, Enrollment


def home(request):
    courses = Course.objects.filter(is_published=True).annotate(
        lesson_count=Count('lessons')
    )[:6]
    categories = Category.objects.annotate(course_count=Count('courses'))
    return render(request, 'home.html', {
        'courses': courses,
        'categories': categories,
    })


def course_list(request):
    courses = Course.objects.filter(is_published=True).annotate(
        lesson_count=Count('lessons')
    )
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    categories = Category.objects.annotate(course_count=Count('courses'))
    return render(request, 'courses/list.html', {
        'courses': courses,
        'categories': categories,
    })


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.annotate(lesson_count=Count('lessons')),
        slug=slug, is_published=True
    )
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course
        ).exists()
    return render(request, 'courses/detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    })


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    lessons = course.lessons.all()
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
    })


@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f'You have enrolled in "{course.title}"')
    return redirect('course_detail', slug=slug)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
