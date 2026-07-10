from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Course, Category, Lesson, Enrollment


def home(request):
    total_courses = Course.objects.filter(is_published=True).count()
    courses = Course.objects.filter(is_published=True).annotate(
        lesson_count=Count('lessons')
    )[:6]
    categories = Category.objects.annotate(course_count=Count('courses'))
    return render(request, 'home.html', {
        'courses': courses,
        'categories': categories,
        'total_courses': total_courses,
    })


def course_list(request):
    courses = Course.objects.filter(is_published=True).annotate(
        lesson_count=Count('lessons')
    )
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )
    categories = Category.objects.annotate(course_count=Count('courses'))
    paginator = Paginator(courses, 9)
    page = request.GET.get('page')
    courses_page = paginator.get_page(page)
    return render(request, 'courses/list.html', {
        'courses': courses_page,
        'categories': categories,
        'query': query,
        'current_category': category_slug,
    })


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.annotate(lesson_count=Count('lessons')),
        slug=slug, is_published=True
    )
    lessons = course.lessons.all()
    is_enrolled = False
    completed_lessons = []
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(
            student=request.user, course=course
        ).first()
        is_enrolled = enrollment is not None
        if is_enrolled:
            completed_lessons = enrollment.completed_lessons or []
    total_lessons = lessons.count()
    completed_count = len(completed_lessons)
    progress = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
    return render(request, 'courses/detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'completed_lessons': completed_lessons,
        'progress': progress,
        'completed_count': completed_count,
    })


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = Enrollment.objects.filter(
        student=request.user, course=course
    ).first()
    if not enrollment:
        messages.warning(request, 'Запишитесь на курс, чтобы получить доступ к урокам.')
        return redirect('course_detail', slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    lessons = course.lessons.all()
    completed_lessons = enrollment.completed_lessons or []
    lesson_list = list(lessons)
    current_index = next((i for i, l in enumerate(lesson_list) if l.id == lesson.id), -1)
    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None
    return render(request, 'courses/lesson.html', {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'completed_lessons': completed_lessons,
    })


@login_required
def lesson_complete(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    completed = enrollment.completed_lessons or []
    if lesson.id not in completed:
        completed.append(lesson.id)
        enrollment.completed_lessons = completed
        enrollment.save()
        messages.success(request, f'Урок "{lesson.title}" завершён!')
    next_lesson = Lesson.objects.filter(course=course, order__gt=lesson.order).first()
    if next_lesson:
        return redirect('lesson_detail', course_slug=course_slug, lesson_slug=next_lesson.slug)
    return redirect('course_detail', slug=course_slug)


@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f'Вы записались на курс "{course.title}"')
    return redirect('course_detail', slug=slug)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').annotate(
        lesson_count=Count('course__lessons')
    )
    for e in enrollments:
        completed = e.completed_lessons or []
        e.completed_count = len(completed)
        e.progress = int((e.completed_count / e.lesson_count * 100)) if e.lesson_count > 0 else 0
    return render(request, 'courses/my_courses.html', {
        'enrollments': enrollments,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
