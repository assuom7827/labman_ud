# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from funding_programs.models import FundingProgram
from funding_programs.forms import FundingProgramForm

from projects.models import Project

# Create your views here.

PAGINATION_NUMBER = 5


#########################
# View: funding_program_index
#########################

def funding_program_index(request):
    funding_programs = FundingProgram.objects.all().order_by('full_name')
    paginator = Paginator(funding_programs, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        funding_programs = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        funding_programs = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        funding_programs = paginator.page(paginator.num_pages)
    return render_to_response("funding_programs/index.html", {
            "funding_programs": funding_programs,
        },
        context_instance = RequestContext(request))


#########################
# View: add_funding_program
#########################

@login_required
def add_funding_program(request):
    if request.method == 'POST':
        form = FundingProgramForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            funding_program = FundingProgram(
                organization = cd['organization'],
                full_name = cd['full_name'].encode('utf-8'),
                short_name = cd['short_name'].encode('utf-8'),
                concession_year = cd['concession_year'],
                geographical_scope = cd['geographical_scope'].encode('utf-8'),
            )

            try:
                funding_program.logo = request.FILES['logo']
            except:
                    pass

            funding_program.save()

            return HttpResponseRedirect(reverse('funding_program_index'))
    else:
        form = FundingProgramForm()

    return render_to_response("funding_programs/add.html", {
            "form": form,
        },
        context_instance = RequestContext(request))


#########################
# View: info_funding_program
#########################

def funding_program_info(request, slug):
    funding_program = get_object_or_404(FundingProgram, slug = slug)
    projects = Project.objects.filter(funding_program = funding_program.id)

    return render_to_response("funding_programs/info.html", {
            "funding_program": funding_program,
            "projects": projects,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_funding_program
#########################

def edit_funding_program(request, slug):
    funding_program = get_object_or_404(FundingProgram, slug = slug)

    if request.method == 'POST':
        form = FundingProgramForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            funding_program.organization = cd['organization']
            funding_program.full_name = cd['full_name'].encode('utf-8')
            funding_program.short_name = cd['short_name'].encode('utf-8')
            funding_program.concession_year = cd['concession_year']
            funding_program.geographical_scope = cd['geographical_scope'].encode('utf-8')

            try:
                funding_program.logo = request.FILES['logo']
            except:
                    pass

            funding_program.save()

            return HttpResponseRedirect(reverse('funding_program_index'))

    else:
        data = {
            'organization': funding_program.organization,
            'full_name': funding_program.full_name,
            'short_name': funding_program.short_name,
            'concession_year': funding_program.concession_year,
            'geographical_scope': funding_program.geographical_scope,
            'logo': funding_program.logo,
        }

        form = FundingProgramForm(initial = data)

    return render_to_response("funding_programs/edit.html", {
            "form": form,
            "funding_program": funding_program,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_funding_program
#########################

@login_required
def delete_funding_program(request, slug):
    funding_program = get_object_or_404(FundingProgram, slug = slug)
    funding_program.delete()

    return HttpResponseRedirect(reverse('funding_program_index'))
